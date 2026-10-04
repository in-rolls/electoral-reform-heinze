# Methods and diagnostic scope

The unadjusted differences reproduce, but several significance claims depend on treating councils elected in the same month as independent. Exact election-month fixed effects cannot identify treatment: all 49 observed election month-year cells are treatment-pure. These checks do not establish that month clustering is the uniquely correct variance model, or that cohort adjustment identifies an electoral-reform effect.

Run `Rscript scripts/inference.R` from the repository root. Inputs are the untouched analysis CSVs. All numbers below are computed in `results/inference/`; outcome differences are direct minus indirect. Baseline estimates reproduce the authors' `original/code/helpers.R::run_regressions`: HC2 for elite/admin outcomes and GP-cluster CR2 for citizen outcomes. The latter retain respondent weighting and do not turn purposive informants into a population sample.

## What dependence changes

The table uses the published Figure 4/5 variables and the reproduced baseline coefficient and p-value. The paper often prints rounded coefficients/significance stars; the p-values below are the precision recovered from its code, not claims that these digits appear in print. Month CR2 uses Satterthwaite degrees of freedom. Wild bootstrap uses 9,999 null-imposed Rademacher draws, `fnw11`, seed 20261002, with inverted 95% intervals.

| Outcome / data variable | Reproduced difference (pp) | Baseline p | Month CR2 p | Month wild p | Wild 95% interval (pp) |
|---|---:|---:|---:|---:|---:|
| Most influential, `most_influential_gd` | 15.068 | .00005 | .01121 | .01960 | [3.166, 24.852] |
| Speaking share, `prop_speakingtime_sarpanch` | 5.195 | .00012 | .00074 | .00250 | [2.380, 7.052] |
| President shared tenure, `resignation` | −20.720 | <.00001 | .04233 | .02970 | [−44.138, −2.093] |
| Citizen shared tenure, `resignation_reported` | −17.971 | <.00001 | .05886 | .03930 | [−40.836, −0.864] |
| President Maratha, `sarpanch_maratha` | 9.804 | .00994 | .04447 | .05641 | [−0.492, 18.618] |
| Pacca house, `pacca_house` | 10.457 | .01129 | .06472 | .10411 | [−3.060, 20.192] |
| Former president/other person leads events, `formersarpanch_otherperson_inauguralevents` | −5.732 | .00018 | .02647 | .05521 | [−9.477, 0.225] |
| Land held by president's caste, `avg_prop_land_held_sarpanch_caste` | 15.418 | <.00001 | .00209 | .00010 | [7.599, 21.419] |

The procedure changes uncertainty, not coefficients. Three wild-bootstrap intervals include zero where the original inference rejected zero at 5%. The two p-values near .055 are borderline: their Monte Carlo standard errors are about .0023 (roughly ±.0045 at 95%). Crossing .05 is not strong evidence that these associations are absent. Citizen shared tenure is also borderline and differs across the two small-sample procedures; the two methods give different uncertainty assessments for that contrast. President authority measures remain positive under both procedures. Unopposed selection and rich-landowner influence also retain their signs and rejection of zero; this does not resolve the separate measurement concerns.

There are 26 direct-election and 23 indirect-election month clusters in the full survey. These 49 election-month groups are not the study's 25 talukas. Size is very uneven: January 2021 contains 153 of 604 GPs; October 2017 contains 72. Consequently the CR2 effective degrees of freedom are about 9.7 rather than 48; the land subsample has 31 clusters and df 4.817. Neither clustered procedure allows arbitrary correlation across months or supplies random assignment. Wild p=0 in the CSV means no simulated statistic was as extreme among 9,999 draws; report it as p<1/9,999 at the simulation's resolution, not literally zero. The plug-in Monte Carlo SE column is also zero at this boundary and is not evidence of zero simulation uncertainty.

For citizens, GPs are nested within election month. `nested_clusters.csv` verifies that two-way month × GP HC1 covariance equals month-only HC1 covariance to floating-point tolerance. Calling this an additional independent robustness check would be misleading. It is an algebraic identity here.

## What election-cohort adjustment can and cannot identify

The full sample month-FE design matrix has 50 columns and rank 49; adding treatment to the 49-column cohort matrix does not increase rank. The same failure occurs for every outcome, including the land subsample (32 columns, rank 31). `cohort_rank.csv` records this directly. No arbitrary coefficient from a dropped dummy or generalized inverse is reported.

Annual fixed effects retain variation only in 2017 (5 indirect, 148 direct councils) and 2020 (8 indirect, 1 direct). Other years contribute no within-year treatment comparison. Among nonmissing land outcomes, the overlap is 3 indirect/109 direct in 2017 and 8 indirect/1 direct in 2020. Thus annual-FE estimates depend heavily on a handful of councils and compare a different, poorly supported contrast.

| Outcome | Baseline difference (pp) | Year-FE difference (pp) | Year-FE SE (pp), baseline variance method | Linear election-month trend difference (pp) |
|---|---:|---:|---:|---:|
| President shared tenure, `resignation` | −20.720 | −1.583 | 22.904 | −24.444 |
| Speaking share, `prop_speakingtime_sarpanch` | 5.195 | 1.455 | 2.753 | 5.206 |
| Caste land, `avg_prop_land_held_sarpanch_caste` | 15.418 | 0.432 | 13.550 | 18.984 |
| Most influential, `most_influential_gd` | 15.068 | 42.237 | 5.667 | 14.687 |

Annual adjustment does not uniformly reduce estimates: the influence coefficient increases sharply. These results diagnose limited support, not a preferred correction. The linear trend leaves or enlarges several gaps, but imposes a single straight line over election time despite regime reversals. It is a functional-form sensitivity check. Without survey dates, election month cannot be separated into calendar effects and individual months since election.

## Single-cohort influence

`leave_one_month_out.csv` fits all 17 survey outcomes after deleting each available election-month cohort; `leaveout_ranges.csv` summarizes the coefficient ranges. Every range preserves the unadjusted sign. Selected differences in percentage points:

| Outcome | Baseline | Smallest to largest deletion estimate |
|---|---:|---:|
| Most influential | 15.068 | 9.940 to 16.233 |
| Speaking share | 5.195 | 4.495 to 5.569 |
| President shared tenure | −20.720 | −30.747 to −17.847 |
| Citizen shared tenure | −17.971 | −27.270 to −15.526 |
| Caste land | 15.418 | 13.966 to 16.976 |

Removing January 2021 makes the president shared-tenure gap more negative (−30.747 pp), consistent with the late indirect cohort having much lower shared-tenure prevalence. This is substantial composition sensitivity, although it does not reverse the association. Leaveout p-values use the original HC2/GP-CR2 variance method; they are not a second month-cluster analysis.

## Limits and verification

The released analysis files lack district/taluka identifiers and survey dates. The admin file additionally lacks election and record dates and GP identifiers. District/taluka fixed effects, geography clustering, geography leaveouts, and administrative exposure adjustment cannot be performed from these files. Numeric ID prefixes are not validated geographic codes. In particular, GP × month nesting does not substitute for taluka × month inference.

The admin HC2 baseline reproduces −13.751 pp (N=1,366, SE 1.695 pp), but this is a cumulative binary comparison with unknown exposure duration. A survival or rate estimate requires those dates. The raw file has 1,425 rows; estimation requires both nonmissing outcome and treatment.

Local validation checks raw means against coefficients, citizen joins without row loss, bootstrap sample/draw counts, independent agreement between `estimatr` CR2 and `clubSandwich` Satterthwaite results, rank failure, nested covariance identity, and complete finite output. `results/inference/validation.txt` records success; `lint.log` records default `lintr` validation. Software versions are in `session-info.txt`.

APIs were checked against official documentation: [estimatr `lm_robust`](https://declaredesign.org/r/estimatr/reference/lm_robust.html), [fwildclusterboot `boottest.lm`](https://s3alfisc.github.io/fwildclusterboot/reference/boottest.lm.html), [clubSandwich `coef_test`](https://jepusto.github.io/clubSandwich/reference/coef_test.html), and the installed `sandwich::vcovCL` manual (the official web endpoint timed out). Both R's and dqrng's random generators are seeded, as required for the chosen bootstrap engine.


## Scope and data limits

The audit covers all 18 headline observational outcomes: 17 survey measures and the
separate administrative resignation indicator. Raw means, denominators, missingness and
original-method uncertainty are in [raw-means.csv](../results/audit/raw-means.csv).
Council identifiers are unique, and the citizen-to-council join preserves all 3,658
respondents. Missing outcomes are excluded rather than recoded as zero. Citizen results
use purposively selected informants; [equal-council weighting](../results/audit/citizen-equal-gp-weight.csv)
is a separate descriptive estimand.

Control-group levels are interpreted independently of model sensitivity. Early indirect
shared tenure is 66/158 (41.77%), versus 20/211 (9.48%) in later indirect councils.
The within-regime difference requires a timing, measurement or institutional account;
its size alone does not establish an error. Unopposed reports remain near 40% in both
indirect cohorts. The [cohort results](cohorts.md) distinguish these patterns from changes
in the direct cohort.

The release contains constructed observational variables, without original responses or
their cleaning program. The separate vignette includes raw data and cleaning code.
Unreleased interview dates, original council term starts, event/censoring dates and
geographic identifiers prevent equal-exposure comparisons, geography clustering and
geography fixed effects. Meeting attendance and full actor responses are also unavailable.
The [data dictionary](data-dictionary.md) identifies the missing fields for each measure.

## Exploratory diagnostic choices

The audit diagnostics were selected after inspecting the published results. They are
exploratory and are not a preregistration. The [diagnostics](diagnostics.md) retain all
17 original sensitivity models and 51 gender-quota bounds, both treatment-side and
outcome-side associations, and equal-strength robustness values. No alternative benchmark
was selected to obtain a preferred conclusion. These ordinary linear-model sensitivity
calculations do not inherit the main models' robust or clustered standard errors.

The five authority comparisons within SC-reserved councils and all direct treatment-by-SC
interaction tests are retained. Within-SC gains test whether the observed pattern requires
Maratha officeholding; they do not isolate class selection, mediation, or amplification
by reservation. The experiment reconciliation retains all six planned contrasts, adjusted
and unadjusted, and distinguishes raw, assigned, observed-outcome and adjusted samples.

The experimental balance check was added after inspecting Table F.3's large HC2 joint
statistics. All four condition regressions are shown with original HC2, ordinary F tests,
and a diagnostic exclusion of seven respondents in sparse religion categories. Their
exclusion localizes the statistic; substantive estimates retain all eligible respondents.
The respondent-gender contingency imbalance is also reported. Neither this sensitivity
nor a nonsignificant balance test verifies assignment implementation.

## Cohort restrictions

Existing transition estimates and raw tabulations were inspected before the recent-cohort
comparisons were specified. The analysis retains all 17 survey outcomes for five rules:
all direct councils plus indirect councils elected in 2020 or later; then elections from
2018, 2019, 2020 and 2021 onward in both regimes. The first is the paper's later-transition
contrast. Each subsequent cutoff narrows the calendar window and reduces direct support.

Inference is withheld when either arm has fewer than two observed councils. Multiple
citizen respondents from one council cannot supply additional independent councils.
Supported comparisons retain original-method HC2/GP-CR2, election-month CR2 and the
null-imposed wild bootstrap with 9,999 requested Rademacher draws, seed 20261003.
Actual draw counts, cluster counts and effective degrees of freedom are reported.
All outcomes are retained regardless of sign or significance. No multiplicity-adjusted
confirmatory interpretation is claimed.

These restrictions concern the recorded incumbent's election year, not interview waves,
verified term starts or equal time at risk. Administrative records lack the necessary dates
and are excluded from these restrictions. The yearly counts and shared-tenure/unopposed
cross-tab check the early rates without assuming that a surprising rate is a coding error.
