"""Report election-cohort restrictions without selecting outcomes by significance."""

from report_utils import ROOT, pct, rows

LABELS = {
    "most_influential_gd": "President most influential",
    "prop_speakingtime_sarpanch": "President speaking share",
    "i_decide_masik_sabha": "President says they decide",
    "sarpanch_maratha": "Maratha president",
    "avg_prop_land_held_sarpanch_caste": "President caste's estimated land share",
    "sarpanch_male": "Male president",
    "sarpanch_land_own_name": "President owns/plans to inherit land",
    "three_four_wheeler": "Household large vehicle",
    "pacca_house": "Pacca dwelling",
    "sarpanch_uncontested": "President unopposed",
    "resignation": "President reports shared tenure",
    "rich_landowner_influences_gp": "President reports landowner influence",
    "sarpanch_nominate_BDO": "Citizen nominates president to bureaucrat",
    "sarpanch_inauguralevents": "Citizen says president leads events",
    "other_nominate_BDO": "Citizen nominates outsider to bureaucrat",
    "formersarpanch_otherperson_inauguralevents": "Citizen says former/other leads events",
    "resignation_reported": "Citizen reports shared tenure",
}


def pvalue(value):
    return "<.0001" if float(value) < 0.0001 else f"{float(value):.4f}"


def main():
    estimates = {
        (r["specification"], r["variable"]): r
        for r in rows("results/recent/estimates.csv")
    }
    baseline = {r["variable"]: r for r in rows("results/audit/raw-means.csv")}
    cohorts = {
        (r["variable"], r["period"]): r for r in rows("results/audit/cohort-means.csv")
    }
    support = {
        (r["specification"], r["direct"]): r for r in rows("results/recent/support.csv")
    }
    yearly = {
        (r["variable"], r["year"], r["direct"]): r
        for r in rows("results/recent/yearly-counts.csv")
    }
    names = {
        "drop_early_indirect": "All direct + later indirect",
        "since_2018": "Elections 2018 onward, both arms",
        "since_2019": "Elections 2019 onward, both arms",
        "since_2020": "Elections 2020 onward, both arms",
        "since_2021": "Elections 2021 onward, both arms",
    }
    support_table = []
    for specification, label in names.items():
        indirect, direct = (support[specification, arm] for arm in ("0", "1"))
        support_table.append(
            f"| {label} | {indirect['councils']} / {direct['councils']} | "
            f"{indirect['election_months']} / {direct['election_months']} |"
        )
    raw_table = []
    for variable in ("resignation", "resignation_reported", "sarpanch_uncontested"):
        cells = [
            f"{pct(cohorts[variable, period]['mean'])}% "
            f"({cohorts[variable, period]['sum']}/{cohorts[variable, period]['n']})"
            for period in ("early_indirect", "direct", "late_indirect")
        ]
        raw_table.append(f"| {LABELS[variable]} | " + " | ".join(cells) + " |")
    comparison_table = []
    core = (
        "resignation",
        "resignation_reported",
        "most_influential_gd",
        "prop_speakingtime_sarpanch",
        "sarpanch_uncontested",
        "sarpanch_inauguralevents",
        "rich_landowner_influences_gp",
    )
    for variable in core:
        cells = [pct(baseline[variable]["difference"])]
        for specification in ("drop_early_indirect", "since_2018", "since_2019"):
            result = estimates[specification, variable]
            cells.append(pct(result["difference"]))
        comparison_table.append(f"| {LABELS[variable]} | " + " | ".join(cells) + " |")

    all_tables = []
    for specification in ("drop_early_indirect", "since_2018", "since_2019"):
        table = []
        for variable, label in LABELS.items():
            result = estimates[specification, variable]
            table.append(
                f"| {label} | {result['indirect_n']} / {result['direct_n']} | "
                f"{pct(result['indirect_mean'])} / {pct(result['direct_mean'])} | "
                f"{pct(result['difference'])} [{pct(result['month_low'])}, "
                f"{pct(result['month_high'])}] | {pvalue(result['baseline_p'])} | "
                f"{pvalue(result['month_p'])} | {pvalue(result['wild_p'])} |"
            )
        all_tables.append(
            f"### {names[specification]}\n\n"
            "| Outcome | Observed N, indirect / direct | Means %, indirect / direct | "
            "Direct minus indirect [month CR2 95% CI], pp | Original-method p | "
            "Month CR2 p | Wild p |\n"
            "|---|---:|---:|---:|---:|---:|---:|\n" + "\n".join(table)
        )
    president = estimates["drop_early_indirect", "resignation"]
    citizen = estimates["drop_early_indirect", "resignation_reported"]
    president_shrink = 1 - float(president["difference"]) / float(
        baseline["resignation"]["difference"]
    )
    citizen_shrink = 1 - float(citizen["difference"]) / float(
        baseline["resignation_reported"]["difference"]
    )
    recent_president = estimates["since_2019", "resignation"]
    recent_influence = estimates["since_2019", "most_influential_gd"]
    recent_speech = estimates["since_2019", "prop_speakingtime_sarpanch"]
    land = estimates["since_2019", "avg_prop_land_held_sarpanch_caste"]
    year_2015 = yearly["resignation", "2015", "0"]
    note = f"""# What survives when older election cohorts are removed?

**The timing concern is severe for reported shared tenure. Several other associations
survive.** Removing early indirect councils reduces the president-reported gap by
{100 * president_shrink:.1f}% and the citizen-reported gap by {100 * citizen_shrink:.1f}%.
Removing older direct councils as well weakens perceived influence substantially.
Speaking share, unopposed selection and citizen-reported event leadership remain different
in the recent comparisons, though precision depends on the inference method.

All 17 survey outcomes and all specified restrictions are retained below. See the
[decision record](methods.md#cohort-restrictions) and [complete output](../results/recent/estimates.csv).

## 1. The high early rates are real summaries of the deposited variables

| Outcome | Early indirect | All direct | Later indirect |
|---|---:|---:|---:|
{chr(10).join(raw_table)}

“Early indirect” follows the author's definition and includes five early-2017 councils;
it is not literally all pre-2017. Later indirect means election year 2020 or 2021.
Citizen denominators count purposive informants, not independent councils.

The president's early shared-tenure rate is not an estimate based on a few observations:
{year_2015['positive']} of the positive early reports come from the
{year_2015['total']} councils elected in 2015 alone. Their rate is
{pct(year_2015['mean'])}% ({year_2015['positive']}/{year_2015['n']}).
Both shared tenure and unopposed selection happen to have 63 positive observations in
2015, but they are not duplicate variables: 27 councils report shared tenure without
unopposed selection and 27 the reverse. [Yearly counts](../results/recent/yearly-counts.csv)
and [early cross-tab](../results/recent/early-cross-tab.csv).

The [survey item](data-dictionary.md) includes **past or planned tenure sharing**. Consequently,
41.8% is not evidence that 41.8% of the interviewed presidents had already resigned.
The counts reproduce the analytical variables; individual responses cannot be validated from this release.
Raw construction files and the separate response categories remain unavailable.

The within-indirect decline is about 32 percentage points for both tenure measures, while
unopposed selection remains near 40%. That is a specific timing/measurement problem for
shared tenure, not a general collapse of every early-indirect outcome. President speaking
and influence levels also barely differ between early and late indirect councils; the
weaker influence result below arises when older *direct* councils are removed.

## 2. “Latest period” has several meanings, with very different support

| Restriction | Councils, indirect / direct | Election-month clusters, indirect / direct |
|---|---:|---:|
{chr(10).join(support_table)}

The first restriction removes old controls but keeps the entire 2017–20 direct cohort.
The next two require both arms to meet the calendar cutoff. From 2020 onward there is
only one direct council, and 2021 has no direct council. No regression uncertainty is
reported for those two unsupported comparisons, including citizen regressions that would
otherwise treat multiple respondents from the same lone council as extra support.
Administrative resignation data have no dates and cannot be filtered this way.

These are **election-year restrictions**, not latest-interview-wave restrictions or
equal-exposure comparisons. Interview dates were not released. All later indirect councils
are compared with earlier direct councils even in the 2019-onward sample, so the filter
does not separate calendar time or term age from election method.

## 3. Effect sizes as the comparison becomes more recent

All entries are **direct minus indirect, in percentage points**. An attenuation percentage
describes the change in this contrast; it is not an estimate of the share of a causal effect
explained by confounding.

| Outcome | Original pooled | Drop early indirect only | Both arms 2018 onward | Both arms 2019 onward |
|---|---:|---:|---:|---:|
{chr(10).join(comparison_table)}

With all direct councils retained, president shared tenure falls from a 20.72-point pooled
gap to {abs(float(president['difference'])) * 100:.2f} points. That smaller contrast remains
distinguishable from zero under the original, month-CR2 and wild-bootstrap conventions.
Citizen shared tenure falls to {abs(float(citizen['difference'])) * 100:.2f} points;
its inference is method-sensitive (month CR2 p={pvalue(citizen['month_p'])},
wild p={pvalue(citizen['wild_p'])}).

With both arms restricted to 2019 onward, president shared tenure is
{pct(recent_president['direct_mean'])}% versus {pct(recent_president['indirect_mean'])}%,
a difference of {pct(recent_president['difference'])} pp with month-CR2 95% CI
[{pct(recent_president['month_low'])}, {pct(recent_president['month_high'])}].
Perceived influence differs by {pct(recent_influence['difference'])} pp,
CI [{pct(recent_influence['month_low'])}, {pct(recent_influence['month_high'])}].
Both estimates shrink and become imprecise; neither proves zero effect.

Speaking share stays positive at {pct(recent_speech['difference'])} pp. Its original HC2
p-value is {pvalue(recent_speech['baseline_p'])}, versus
{pvalue(recent_speech['month_p'])} with month CR2 and
{pvalue(recent_speech['wild_p'])} with the bootstrap. Thus it is not uniformly below .05
under every convention. Unopposed selection and citizen-reported event leadership remain
clearer across these conventions. Landowner influence reports also fall, but none of the
27 recent direct presidents reports influence; that small zero cell deserves care.

The caste-land difference becomes larger, not smaller, under the recent restriction:
{pct(land['difference'])} pp. But only {land['direct_n']} direct councils have the measure,
with {land['direct_months']} direct election-month clusters. Its month-CR2 p-value is
{pvalue(land['month_p'])}, versus bootstrap p={pvalue(land['wild_p'])}.
This is an increase in the estimated difference with fragile precision, not disappearance
of the composition association.

## 4. All outcomes, denominators and inference

Original-method inference uses HC2 for council outcomes and GP CR2 for citizen outcomes.
Month CR2 clusters on election month–year and uses small-sample degrees of freedom;
an independent `clubSandwich` calculation agrees. All later-indirect councils occupy only
five month clusters, mostly January/February 2021. Many month-CR2 tests have only about
four or five effective degrees of freedom. Neither clustering nor bootstrapping fixes
cohort confounding or guarantees reliable inference with this concentration.

Wild inference uses null-imposed Rademacher weights, fnw11, seed 20261003, and requests
9,999 draws. For the 2019-onward land outcome, all 2,048 possible draws across 11 clusters
are enumerated instead; its Monte Carlo sampling error is zero conditional on that
bootstrap distribution. Actual draw counts, MC SEs, bootstrap intervals, month degrees
of freedom and all missingness denominators are in the CSV. The table does not apply a
multiplicity correction, and values near .05 are not treated as categorical verdicts.

{(chr(10) * 2).join(all_tables)}

The empirical conclusion is therefore outcome-specific: the dramatic pooled rotation
gap is heavily dependent on the early indirect cohort; the influential-actor difference
depends substantially on older direct councils; several other reported associations
persist. Missing interview and council-history dates prevent a comparison at equal
term age, and the very latest election years cannot support a two-regime comparison.
"""
    (ROOT / "docs/cohorts.md").write_text(note)


if __name__ == "__main__":
    main()
