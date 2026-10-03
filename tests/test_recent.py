"""Independent sample restrictions, raw contrasts and inference-support checks."""

import math
import statistics
import unittest

from test_audit import present, read_csv


class RecentCohortTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.elite = read_csv("original/data/analysis/elite_survey.csv")
        cls.by_id = {r["r_villageid"]: r for r in cls.elite}
        cls.citizen = read_csv("original/data/analysis/citizen_survey.csv")
        cls.estimates = read_csv("results/recent/estimates.csv")

    def selected(self, result):
        data = self.elite if result["source"] == "elite" else self.citizen
        selected = []
        for row in data:
            year = int(self.by_id[row["r_villageid"]]["sarpanch_election_year"])
            include = (
                row["direct"] == "1" or year >= 2020
                if result["specification"] == "drop_early_indirect"
                else year >= int(result["specification"].split("_")[1])
            )
            if include:
                selected.append(row)
        return selected

    def test_all_restrictions_means_counts_and_hc2(self):
        self.assertEqual(len(self.estimates), 85)
        for result in self.estimates:
            with self.subTest(spec=result["specification"], outcome=result["variable"]):
                selected = self.selected(result)
                variable = result["variable"]
                groups = {}
                for arm, prefix in (("0", "indirect"), ("1", "direct")):
                    observed = [
                        r
                        for r in selected
                        if r["direct"] == arm and present(r[variable])
                    ]
                    groups[arm] = [float(r[variable]) for r in observed]
                    self.assertEqual(len(observed), int(result[f"{prefix}_n"]))
                    self.assertEqual(
                        len({r["r_villageid"] for r in observed}),
                        int(result[f"{prefix}_gp"]),
                    )
                    if observed:
                        self.assertAlmostEqual(
                            statistics.mean(groups[arm]),
                            float(result[f"{prefix}_mean"]),
                            places=12,
                        )
                if all(groups.values()):
                    self.assertAlmostEqual(
                        statistics.mean(groups["1"]) - statistics.mean(groups["0"]),
                        float(result["difference"]),
                        places=12,
                    )
                if result["source"] == "elite" and result["status"] == "estimated":
                    variance = sum(
                        statistics.variance(g) / len(g) for g in groups.values()
                    )
                    self.assertAlmostEqual(
                        math.sqrt(variance), float(result["baseline_se"]), places=12
                    )

    def test_primary_restriction_equals_existing_transition(self):
        transitions = {
            r["variable"]: r
            for r in read_csv("results/audit/transition-contrasts.csv")
            if r["comparison"] == "late_vs_direct"
        }
        for result in self.estimates:
            if result["specification"] != "drop_early_indirect":
                continue
            existing = transitions[result["variable"]]
            self.assertAlmostEqual(
                float(result["difference"]), float(existing["difference"]), places=12
            )
            self.assertAlmostEqual(
                float(result["baseline_se"]), float(existing["se"]), places=12
            )

    def test_latest_period_does_not_manufacture_independent_support(self):
        for result in self.estimates:
            if result["specification"] not in ("since_2020", "since_2021"):
                continue
            self.assertEqual(result["status"], "insufficient_support")
            self.assertLessEqual(int(result["direct_gp"]), 1)
            for field in ("baseline_p", "month_p", "wild_p", "wild_low", "wild_high"):
                self.assertFalse(present(result[field]))
        support = {
            (r["specification"], r["direct"]): int(r["councils"])
            for r in read_csv("results/recent/support.csv")
        }
        self.assertEqual(support["since_2020", "1"], 1)
        self.assertEqual(support["since_2021", "1"], 0)
        self.assertEqual(support["since_2019", "1"], 27)

    def test_bootstrap_records_actual_draw_space(self):
        for result in self.estimates:
            if result["status"] != "estimated":
                continue
            clusters = int(result["direct_months"]) + int(result["indirect_months"])
            draws = int(result["wild_draws"])
            self.assertEqual(draws, min(9999, 2**clusters))
            if result["wild_full_enumeration"] == "TRUE":
                self.assertEqual(float(result["wild_mc_se"]), 0)
                self.assertEqual(draws, 2**clusters)
            self.assertEqual(int(result["wild_seed"]), 20261003)


if __name__ == "__main__":
    unittest.main()
