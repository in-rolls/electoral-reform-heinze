"""Independent arithmetic and sample-conservation checks of generated results."""

import csv
import math
import statistics
import unittest
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with (ROOT / path).open(newline="") as stream:
        return list(csv.DictReader(stream))


def present(value):
    return value not in ("", "NA")


class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {
            source: read_csv(f"original/data/analysis/{filename}.csv")
            for source, filename in (
                ("elite", "elite_survey"),
                ("citizen", "citizen_survey"),
                ("admin", "resignation_admin"),
            )
        }
        cls.means = read_csv("results/audit/raw-means.csv")

    def test_counts_and_join_cardinality(self):
        elite = self.data["elite"]
        self.assertEqual(Counter(r["direct"] for r in elite), {"0": 370, "1": 234})
        identifiers = {r["r_villageid"]: r for r in elite}
        self.assertEqual(len(identifiers), 604)
        citizens = self.data["citizen"]
        self.assertEqual(len(citizens), 3658)
        self.assertEqual(len({r["r_villageid"] for r in citizens}), 604)
        for row in citizens:
            self.assertEqual(row["direct"], identifiers[row["r_villageid"]]["direct"])

    def test_every_headline_mean_and_hc2_se(self):
        self.assertEqual(len(self.means), 18)
        for result in self.means:
            with self.subTest(variable=result["variable"]):
                rows = self.data[result["source"]]
                values = {}
                for arm, prefix in (("0", "indirect"), ("1", "direct")):
                    group = [r for r in rows if r["direct"] == arm]
                    values[arm] = [
                        float(r[result["variable"]])
                        for r in group
                        if present(r[result["variable"]])
                    ]
                    self.assertEqual(len(values[arm]), int(result[f"{prefix}_n"]))
                    self.assertEqual(len(group), int(result[f"{prefix}_total"]))
                    self.assertAlmostEqual(
                        statistics.mean(values[arm]), float(result[f"{prefix}_mean"])
                    )
                self.assertAlmostEqual(
                    statistics.mean(values["1"]) - statistics.mean(values["0"]),
                    float(result["difference"]),
                    places=12,
                )
                if result["source"] != "citizen":
                    se = math.sqrt(
                        sum(statistics.variance(v) / len(v) for v in values.values())
                    )
                    self.assertAlmostEqual(se, float(result["se"]), places=12)

    def test_admin_exclusions_are_not_zeros(self):
        rows = self.data["admin"]
        self.assertEqual(len(rows), 1425)
        self.assertEqual(sum(not present(r["direct"]) for r in rows), 56)
        retained = [r for r in rows if present(r["direct"]) and present(r["resigned"])]
        self.assertEqual(len(retained), 1366)
        self.assertEqual(
            Counter((r["direct"], r["resigned"]) for r in retained),
            {("0", "0"): 652, ("0", "1"): 156, ("1", "0"): 527, ("1", "1"): 31},
        )

    def test_land_missingness_concentrated_in_early_cohort(self):
        observed = Counter()
        totals = Counter()
        for row in self.data["elite"]:
            period = (
                "direct"
                if row["direct"] == "1"
                else "early" if int(row["sarpanch_election_year"]) <= 2017 else "late"
            )
            totals[period] += 1
            observed[period] += present(row["avg_prop_land_held_sarpanch_caste"])
        self.assertEqual(totals, {"early": 159, "direct": 234, "late": 211})
        self.assertEqual(observed, {"early": 6, "direct": 167, "late": 209})

    def test_category_partition_and_missingness(self):
        for a, b in (
            ("sarpanch_nominate_BDO", "other_nominate_BDO"),
            ("sarpanch_inauguralevents", "formersarpanch_otherperson_inauguralevents"),
        ):
            residual = 0
            for row in self.data["citizen"]:
                self.assertEqual(present(row[a]), present(row[b]))
                if present(row[a]):
                    self.assertIn(int(row[a]) + int(row[b]), (0, 1))
                    residual += row[a] == row[b] == "0"
            self.assertGreater(residual, 0)

    def test_exact_month_fixed_effects_cannot_identify_treatment(self):
        groups = defaultdict(set)
        for row in self.data["elite"]:
            groups[row["sarpanch_election_year"], row["sarpanch_election_month"]].add(
                row["direct"]
            )
        self.assertEqual(len(groups), 49)
        self.assertTrue(all(len(arms) == 1 for arms in groups.values()))
        ranks = read_csv("results/inference/cohort_rank.csv")
        self.assertEqual(len(ranks), 17)
        self.assertTrue(all(r["treatment_identified"] == "FALSE" for r in ranks))

    def test_author_artifacts_and_baselines(self):
        rows = read_csv("results/authors/artifact-comparison.csv")
        tables = [r for r in rows if r["artifact"].endswith(".tex")]
        self.assertEqual(len(tables), 28)
        self.assertTrue(all(r["numeric_values_different"] == "0" for r in tables))
        self.assertEqual(sum(int(r["numeric_values_original"]) for r in tables), 2925)
        figure_labels = read_csv("results/authors/main-figure-label-comparison.csv")
        self.assertEqual(len(figure_labels), 161)
        self.assertTrue(
            all(r["matches_printed_precision"] == "TRUE" for r in figure_labels)
        )
        independent = {r["variable"]: r for r in self.means}
        baselines = [
            r
            for r in read_csv("results/inference/estimates.csv")
            if r["specification"].startswith("baseline_")
        ]
        self.assertEqual(len(baselines), 18)
        for result in baselines:
            reference = independent[result["outcome"]]
            self.assertAlmostEqual(
                float(result["estimate"]), float(reference["difference"])
            )
            self.assertAlmostEqual(float(result["se"]), float(reference["se"]))


if __name__ == "__main__":
    unittest.main()
