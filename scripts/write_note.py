"""Generate the concise audit note from verified numerical outputs."""

from report_utils import ROOT, pct, rows


def main():
    means = {r["variable"]: r for r in rows("results/audit/raw-means.csv")}
    cohorts = {
        (r["variable"], r["period"]): r for r in rows("results/audit/cohort-means.csv")
    }
    boot = {r["outcome"]: r for r in rows("results/inference/wild_bootstrap.csv")}
    inference = {
        (r["outcome"], r["specification"]): r
        for r in rows("results/inference/estimates.csv")
    }
    transitions = {
        (r["variable"], r["comparison"]): r
        for r in rows("results/audit/transition-contrasts.csv")
    }
    bounds = {r["direct"]: r for r in rows("results/audit/land-bounds.csv")}
    authority = {
        (r["variable"], r["quota"]): r
        for r in rows("results/audit/authority-benchmark.csv")
    }
    land_low = float(bounds["1"]["lower"]) - float(bounds["0"]["upper"])
    land_high = float(bounds["1"]["upper"]) - float(bounds["0"]["lower"])
    table = []
    for variable, published in (
        ("prop_speakingtime_sarpanch", "25.9 → 31.1"),
        ("most_influential_gd", "17.8 → 32.9"),
        ("resignation", "23.3 → 2.6"),
        ("resignation_reported", "21.0 → 3.0"),
        ("resigned", "19.3; difference −13.8 pp"),
        ("rich_landowner_influences_gp", "13.1; difference −8.3 pp"),
        ("sarpanch_uncontested", "40.9; difference −28.1 pp"),
        ("avg_prop_land_held_sarpanch_caste", "28.9; difference +15.4 pp"),
    ):
        r = means[variable]
        table.append(
            f"| `{variable}` | {published} | {pct(r['indirect_mean'])} → "
            f"{pct(r['direct_mean'])} | {r['indirect_n']} / {r['direct_n']} |"
        )
    cohort_table = []
    for variable, label in (
        ("resignation", "President shared tenure"),
        ("resignation_reported", "Citizen shared tenure"),
        ("sarpanch_uncontested", "Unopposed"),
    ):
        cells = []
        for period in ("early_indirect", "direct", "late_indirect"):
            r = cohorts[variable, period]
            cells.append(f"{pct(r['mean'])}% ({r['sum']}/{r['n']})")
        cohort_table.append(f"| {label} | " + " | ".join(cells) + " |")
    inference_table = []
    for variable, label in (
        ("sarpanch_maratha", "Maratha president"),
        ("pacca_house", "Pacca dwelling"),
        ("formersarpanch_otherperson_inauguralevents", "Former/other leads events"),
        ("resignation_reported", "Citizen shared tenure"),
    ):
        r = means[variable]
        b = boot[variable]
        c = inference[variable, "election_month_CR2"]
        baseline_p = "<.00001" if float(r["p"]) < 0.00001 else f"{float(r['p']):.5f}"
        inference_table.append(
            f"| {label} (`{variable}`) | {pct(r['difference'])} pp | "
            f"{baseline_p} | {float(c['p']):.5f} | "
            f"{float(b['p']):.5f} | [{pct(b['lower'])}, {pct(b['upper'])}] |"
        )
    delta = transitions["resignation", "early_vs_late"]
    speech = authority["prop_speakingtime_sarpanch", "all"]
    influence = authority["most_influential_gd", "all"]
    note = f"""# Electoral reform: numerical results

The [interpretation of the evidence](interpretation.md) examines the broader causal
argument, statutory changes, sensitivity calibration and preregistration. This note
retains the original four-section numerical audit and its verification boundaries.

The headline numbers reproduce. They describe a set of
differences in presidential voice, characteristics, and reported rotation across election
regimes. The public deposit cannot establish comparable resignation exposure, separate
reform effects from unrestricted cohort effects, or recover the full actor distributions.
One small descriptive-SE error is verified; several larger concerns are measurement or
identification limitations rather than coding errors.

Sources: [article](https://doi.org/10.1017/S0003055425101068),
[replication v1.0](https://doi.org/10.7910/DVN/QGH7P4), and the
[preserved file manifest](../sources/file-manifest.csv). Percentages below are levels;
differences are percentage points (pp). “Early indirect” follows the author's definition
(indirect and election year ≤2017), including five 2017 councils.

## A. What reproduces exactly

The unchanged R workflow reproduces all **28 deposited tables / 2,925 printed numerical
cells** and **161 checked labels in main Figures 3–6**. All 12 deposited figures regenerate.
Figure 2's underlying election counts are exported; exhaustive numerical recovery from its
unlabelled bars and the appendix rasters is not claimed. R 4.6.0 was available, versus the
author's 4.4.3; missing packages were installed locally, with no author-code edits.
[Execution record and coverage](reproduction.md).

| Variable | Published, % (Figures 4–5) | Replicated indirect → direct, % | Observed N, indirect / direct |
|---|---:|---:|---:|
{chr(10).join(table)}

There are 604 survey councils (370 indirect, 234 direct) and 3,658 citizen records.
Administrative estimation uses 1,366 of 1,425 released rows: 56 lack treatment and three
additional rows lack the outcome. The actual direct administrative rate is 31/558 = 5.56%;
5.5% is what subtracting the two rounded Figure 5 numbers suggests, not a verified error.
All 18 unadjusted headline coefficients reconcile with raw group means.
[Means, SEs, CIs, missingness and cohort denominators](../results/audit/raw-means.csv).
The vignette's adjusted effects also reproduce: male +4.881 pp and Maratha +13.885 pp,
N=2,341; these concern perceived authority of hypothetical presidents.

## B. Measurement and numerical details

**Verified, minor denominator error.** Figure 3's indirect population mean SE is **223.518**,
reproduced exactly by `helpers.R::ate_lm_robust`, which divides by √370 although
`total_population_gp` has 369 observed indirect values. The correct descriptive SE is
**223.821**. Seven mean-SE cells use oversized denominators; only this changes printed
precision. Difference-in-means coefficients, regression SEs and headline conclusions are
unaffected. [Old/new values](../results/authors/balance-mean-se-denominator-audit.csv).

**Measurement mismatch, not a demonstrated recoding error.** Published “resignation”
23.3% → 2.6% is replicated as 86/369 → 6/232 for `resignation`. The exact president item is
“Was/will your tenure shared/be shared with other members, or did/will you serve for the
full tenure?” The citizen item also includes anticipated turnover. These are shared-tenure
reports, not completed resignation incidence. The original four-category president answer
is absent, so completed versus planned turnover cannot be separated.

**Related construct limits.** Rich-landowner influence reproduces 47/359 → 11/229
(13.09% → 4.80%), but `rich_landowner_influences_gp` is the president's report; the
questionnaire does not explicitly restrict the landowner to an unelected person.
Unopposed selection reproduces 151/369 → 30/234 (40.92% → 12.82%), but
`sarpanch_uncontested` does not specify the ward-election versus presidential-selection
stage. The observed diagnostic is the mismatch between question and claimed construct;
raw stage, reporter-validation and landowner-status fields are absent. These data do not
identify corrected “total elite influence” or comparable-stage competition rates.
The paper acknowledges an alternative explanation for uncontested elections.
[Exact questions, categories and source locations](data-dictionary.md).

**Unresolved timing provenance.** Appendix C.8 describes January 2020 implementation;
the government's February bulletin still describes a prospective ordinance, and the
enacted reversal is gazetted March 5 with transitional exceptions. Two released councils
report February 2020 indirect presidential elections. Removing that month changes
`resignation` from −20.72 to −20.57 pp, so these two records do not drive the pooled gap.
This is a diagnostic, not a corrected estimate: incumbent elections, council terms and
election-process start dates must first be reconciled. The 2020 Act also permits member
selection to fill a directly elected president's vacancy, while survey `direct` records the
incumbent's current mandate. Whether turnover itself changes recorded treatment status
is therefore a further unresolved construction question; affected cases cannot be counted
from the release. [Official sources](institutions.md).

## C. Timing and inference

**Timing changes the contrast.** The published early/direct/late means reproduce:

| Outcome | Early indirect | Direct | Late indirect |
|---|---:|---:|---:|
{chr(10).join(cohort_table)}

The within-indirect president contrast is **{pct(delta['difference'])} pp**
(HC2 95% CI [{pct(delta['ci_low'])}, {pct(delta['ci_high'])}]); the direct-minus-indirect
gap changes from −39.19 pp against early councils to −6.89 pp against late councils.
Both transition comparisons reuse the same direct cohort. This is a cross-cohort comparison,
not observed within-council change, and does not prove that elapsed tenure explains it.
[All transition estimates](../results/audit/transition-contrasts.csv) and
[election-month plot](../results/audit/shared-tenure-by-election-month.png).

All **49 election month–year groups are treatment-pure**: adding treatment to exact cohort
fixed effects leaves rank 49 rather than 50. There is no separately identified month-FE
effect. Year FE changes `resignation` from −20.72 to −1.58 pp (SE 22.90 pp) and land share
from +15.42 to +0.43 pp (SE 13.55 pp), but depends on very sparse within-year overlap;
it is an unstable alternative comparison, not a correction. Influence actually rises under
year FE, so adjustment does not uniformly erase the findings.

**Land missingness changes the represented sample.** Published N=382 and +15.4 pp for
`avg_prop_land_held_sarpanch_caste` reproduce, but coverage is **6/159 early indirect,
167/234 direct, 209/211 late indirect**; all 142 councils elected in 2015 lack it.
Indirect/direct missingness is 41.89%/28.63% (Pearson p=.00135), with much stronger cohort
imbalance. The early comparison is +14.90 pp, SE 12.56 pp; the late comparison remains
+15.43 pp, SE 3.07 pp. The late-cohort association is positive; two equally
informative transition replications do not. Without assumptions about missing values,
the full-sample descriptive difference is bounded by **[{pct(land_low)}, {pct(land_high)}] pp**,
using only the measure's [0,1] support. These are identification bounds, not a confidence
interval. The measure is a bureaucrat's approximate assessment, not land-register acreage.
[Missingness by quota, caste and cohort](../results/audit/land-missingness.csv).

**Dependence changes precision.** The table contrasts reproduced original inference with
election-month CR2 and a null-imposed wild cluster bootstrap (9,999 Rademacher draws,
seed 20261002; coefficients unchanged). Original p-values are recovered from the code;
the paper prints rounded effects and significance thresholds.

| Outcome / variable | Reproduced effect | Original p | Month CR2 p | Wild p | Wild 95% CI, pp |
|---|---:|---:|---:|---:|---:|
{chr(10).join(inference_table)}

The two wild p-values near .055 are borderline (Monte Carlo SE about .0023), not evidence
of no association. Citizen shared tenure is procedure-sensitive. The 49 uneven month
clusters are not the 25 talukas; geographic IDs are unavailable. GP × month clustering
is redundant because GPs nest within months. Every single-month deletion preserves
the original coefficient signs. [Full inference and support diagnostics](methods.md).

**Repeated questions limit independent validation.** The published citizen authority gains
of +8.2/+13.2 pp and outsider declines of −5.2/−5.7 pp reproduce as +8.164/+13.169 and
−5.216/−5.732 pp. The four variables (`sarpanch_nominate_BDO`, `other_nominate_BDO`,
`sarpanch_inauguralevents`, `formersarpanch_otherperson_inauguralevents`) come from two
questions. Released pairs are mutually exclusive, share identical missingness, and leave
residual categories: BDO 24.95% → 22.01%; events 17.86% → 10.42%. They are dependent,
but not exact complements. [Recoverable category distributions](../results/audit/citizen-categories.csv).
Citizen respondents are purposively selected informants, not a random village-population
sample. Equal GP weighting retains all five citizen-result signs; it does not fix selection.

**Exposure audit remains untestable.** The administrative −13.8 pp result reproduces
as −13.751 pp for `resigned`, but no election, resignation or record dates are released.
`months_at_risk` cannot be constructed. Summer-2022 collection and the reform timeline
could imply *longer* exposure for direct councils if those dates map to ongoing terms;
“direct had less time” is not established. Likewise, no survey dates are released, so a
single assumed endpoint for the 2020–22 survey would assign unverified exposure durations. Full actor
distributions, geographic FE/clustering/leaveouts and full citizen multinomial categories
also remain unavailable. [Precise missing artifacts](data-dictionary.md).

## D. Summary of measured differences

**Measured presidential participation is higher under direct elections.** Speaking rises
by {pct(means['prop_speakingtime_sarpanch']['difference'])} pp and perceived influence by
{pct(means['most_influential_gd']['difference'])} pp; month-bootstrap p-values are
{float(boot['prop_speakingtime_sarpanch']['p']):.4f} and
{float(boot['most_influential_gd']['p']):.4f}. These are comparative associations, conditional
on the observational design's assumptions for a causal interpretation.

Direct-president speaking is {pct(speech['mean_direct'])}%
(ordinary one-sample 95% CI {pct(speech['direct_mean_low'])}–{pct(speech['direct_mean_high'])}%),
and most-influential share is {pct(influence['mean_direct'])}%
({pct(influence['direct_mean_low'])}–{pct(influence['direct_mean_high'])}%). Distance from
one-third is −2.27 and −0.43 pp; illustrative one-sample p-values are .0384 and .8897.
One-third is not a substantively justified null: the questionnaire permits relatives,
other participants and “none.” The paper itself notes 31% speaking and distinguishes this from absolute executive
control (p.13, footnote32). Aggregate near-parity also hides heterogeneity: direct
women-reserved councils have 23.33% speaking/16.04% influence, versus 37.46%/46.88% elsewhere.
The speaking treatment differences are +3.09 pp (CI −0.24 to 6.42) and +5.94 pp (2.45 to 9.42);
HC2 interaction tests give p=.246 for speaking and p=.189 for influence, so the
estimated treatment-effect differences across quota groups are not well distinguished.

**Different officeholder characteristics and lower reported rotation remain visible.**
Several demographic/asset associations and the late-cohort caste-land association persist,
as do unopposed and rich-landowner-report differences. They support a narrower account
of who occupies office and what informants report. They do not independently establish
total elite control, institutional mediation, or equal-exposure resignation risk. The
vignette supports an effect of assigned caste/gender cues on hypothetical authority
judgments; the paper itself concedes it is not a mediation test of electoral reform.
"""
    (ROOT / "docs/audit.md").write_text(note)


if __name__ == "__main__":
    main()
