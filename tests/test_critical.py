"""Independently check follow-up samples, contrasts and original registration bytes."""

import hashlib
import json
import math
import statistics
import unittest
from collections import Counter

from test_audit import ROOT, present, read_csv


class CriticalAuditTests(unittest.TestCase):
    def test_experiment_raw_flow_and_recoding(self):
        raw = read_csv("original/data/raw/survey_experiment.csv")
        assigned = [r for r in raw if r["sarpanchgendercaste_combination"] != "NA NA"]
        self.assertEqual(len(raw), 2368)
        self.assertEqual(len(assigned), 2366)
        clean = read_csv("original/data/analysis/survey_experiment_clean.csv")
        self.assertEqual(len(clean), len(assigned))
        for before, after in zip(assigned, clean):
            for source, target, mapping in (
                ("q9.2.1", "authority", {"Sarpanch": "1", "Someone else": "0"}),
                ("q9.2.3", "pliability", {"Resign": "1", "Resist": "0"}),
                (
                    "q9.2.4",
                    "backlash",
                    {"Yes, it is likely": "1", "No, it is not likely": "0"},
                ),
            ):
                self.assertEqual(mapping.get(before[source], "NA"), after[target])
        authority = Counter(r["authority"] for r in clean)
        self.assertEqual(authority, {"1": 1596, "0": 751, "NA": 19})
        for result in read_csv("results/critical/experiment-missingness.csv"):
            group = [
                r
                for r in clean
                if r["Male"] == result["male"] and r["Maratha"] == result["maratha"]
            ]
            self.assertEqual(len(group), int(result["assigned"]))
            self.assertEqual(
                sum(present(r[result["variable"]]) for r in group),
                int(result["observed"]),
            )

    def test_experiment_unadjusted_effects_and_variance(self):
        clean = read_csv("original/data/analysis/survey_experiment_clean.csv")
        for result in read_csv("results/critical/experiment-estimates.csv"):
            if result["adjusted"] != "FALSE":
                continue
            variable, treatment = result["variable"], result["treatment"]
            groups = [
                [
                    float(r[variable])
                    for r in clean
                    if r[treatment] == arm and present(r[variable])
                ]
                for arm in ("0", "1")
            ]
            self.assertEqual(sum(map(len, groups)), int(result["n"]))
            self.assertAlmostEqual(
                statistics.mean(groups[1]) - statistics.mean(groups[0]),
                float(result["estimate"]),
                places=12,
            )
            variance = sum(statistics.variance(g) / len(g) for g in groups)
            self.assertAlmostEqual(math.sqrt(variance), float(result["se"]), places=12)

    def test_sc_effects_and_saturated_interactions(self):
        elite = read_csv("original/data/analysis/elite_survey.csv")
        quota_by_id = {r["r_villageid"]: r["reserved_sc"] for r in elite}
        citizen = read_csv("original/data/analysis/citizen_survey.csv")
        results = read_csv("results/critical/sc-authority.csv")
        for result in results:
            variable = result["variable"]
            source = elite if variable in elite[0] else citizen
            groups = {
                (quota, arm): [
                    float(r[variable])
                    for r in source
                    if quota_by_id[r["r_villageid"]] == quota
                    and r["direct"] == arm
                    and present(r[variable])
                ]
                for quota in ("0", "1")
                for arm in ("0", "1")
            }
            effects = {
                q: statistics.mean(groups[q, "1"]) - statistics.mean(groups[q, "0"])
                for q in ("0", "1")
            }
            if result["comparison"] == "interaction":
                expected = effects["1"] - effects["0"]
                if source is elite:
                    variance = sum(
                        statistics.variance(g) / len(g) for g in groups.values()
                    )
                    self.assertAlmostEqual(
                        math.sqrt(variance), float(result["se"]), places=12
                    )
            else:
                q = result["comparison"][-1]
                expected = effects[q]
                self.assertEqual(len(groups[q, "0"]), int(result["n_indirect"]))
                self.assertEqual(len(groups[q, "1"]), int(result["n_direct"]))
            self.assertAlmostEqual(expected, float(result["estimate"]), places=12)

    def test_preregistration_matches_registered_digest(self):
        folder = ROOT / "sources/preregistration"
        registration = json.loads((folder / "registration.json").read_text())
        attributes = registration["data"]["attributes"]
        attached = attributes["registration_responses"]["q6.uploader"]
        self.assertEqual(len(attached), 1)
        digest = hashlib.sha256((folder / "analysis-plan.pdf").read_bytes()).hexdigest()
        self.assertEqual(digest, attached[0]["file_hashes"]["sha256"])
        self.assertTrue(attributes["date_registered"].startswith("2024-10-18"))

    def test_balance_diagnostic_uses_actual_covariate_complete_cells(self):
        controls = (
            "rural",
            "age",
            "gender",
            "religion",
            "caste",
            "education",
            "prior_vote",
            "knowledge_local_politics",
            "gender_norms",
        )
        data = [
            r
            for r in read_csv("original/data/analysis/survey_experiment_clean.csv")
            if all(present(r[v]) for v in controls)
        ]
        self.assertEqual(len(data), 2359)
        sparse = [r for r in data if r["religion"] in ("Christian", "Jain")]
        self.assertEqual(
            Counter(r["religion"] for r in sparse), {"Christian": 4, "Jain": 3}
        )
        self.assertTrue(all(r["Maratha"] == "0" for r in sparse))
        cells = Counter(
            (r["gender"], r["sarpanchgendercaste_combination"]) for r in data
        )
        row_totals = Counter(r["gender"] for r in data)
        column_totals = Counter(r["sarpanchgendercaste_combination"] for r in data)
        statistic = 0
        for gender, row_total in row_totals.items():
            for condition, column_total in column_totals.items():
                expected = row_total * column_total / len(data)
                statistic += (cells[gender, condition] - expected) ** 2 / expected
        result = read_csv("results/critical/experiment-gender-balance.csv")[0]
        self.assertAlmostEqual(statistic, float(result["statistic"]), places=10)
        self.assertEqual(int(result["df"]), 3)
        p = math.erfc(math.sqrt(statistic / 2)) + math.sqrt(
            2 * statistic / math.pi
        ) * math.exp(-statistic / 2)
        self.assertAlmostEqual(p, float(result["p"]), places=12)


if __name__ == "__main__":
    unittest.main()
