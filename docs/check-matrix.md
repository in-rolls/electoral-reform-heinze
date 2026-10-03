# Audit coverage and unresolved checks

“Verified” refers to a completed numerical or source check. “Unavailable” means the required artifact was searched for throughout the 113-file release and was absent; it is not a null result. The public release contains analytical survey/admin variables, not their raw construction code. The separate experiment does include raw data and cleaning code.

| Requested work | Status and result | Evidence |
|---|---|---|
| Entire deposit preserved | Verified: version 1.0, 113 files; all Dataverse MD5s match; original archive and per-file SHA-256 | `sources/SHA256SUMS`, `sources/file-manifest.csv`, `analysis/preserve.py` |
| Author pipeline unchanged | Completed after local dependency installation; actual R 4.6 versus original 4.4.3 | `docs/execution.md`, `results/authors/` |
| Published numerical reproduction | 28 tables / 2,925 cells and 161 main-figure labels match; all 12 figures regenerate | Artifact and label comparison CSVs; raster-coordinate limitation explicit |
| Question-to-variable mapping | Exact wording/options/respondents and published coding descriptions recorded | `docs/variable-dictionary.md` |
| Raw observational recoding | Unavailable: only constructed analytical columns supplied; no replacement recoding invented | Dictionary per-variable limits |
| Headline means before models | 18 outcomes, group N/means/SE/CI/missingness and three-cohort means; every coefficient equals raw difference | `results/audit/raw-means.csv` |
| Authority actor distributions | President measures verified; vice-president/bureaucrat and other actor categories unavailable | Instrument permits more than three actor categories; dictionary |
| One-third reference and gender quotas | Descriptive distance/ordinary intervals, explicitly illustrative tests, women-reserved versus other councils | `authority-benchmark.csv` |
| Shared-tenure timing | Verified month/year means, plot, three-cohort contrasts, reuse of direct cohort | `shared-tenure-by-election-time.csv`, PNG, `transition-contrasts.csv` |
| Survey dates/months elapsed | Unavailable; survey spans 2020–22, so no single endpoint assumed | Questionnaire election item may denote current incumbent's election, not verified council start |
| Administrative event/exposure audit | Baseline 156/808 versus 31/558 verified; exposure adjustment unavailable | Six columns only; needs term start, event and censor dates, council key |
| Cohort adjustment | Month FE not identified; year FE sparse; linear month trend explicitly functional-form sensitivity | `results/inference/cohort_rank.csv`, `estimates.csv`, `year_support.csv` |
| Dependence and bootstrap | GP baseline reproduced; month CR2 and 9,999-draw wild bootstrap; effective df and Monte Carlo uncertainty reported | `docs/inference.md`, inference CSVs |
| Two-way covariance | GP × month equals month alone because nested; verified numerically | `nested_clusters.csv` |
| Geographic clustering/FE/leaveouts | Unavailable: district/taluka identifiers and crosswalk absent; numeric GP prefixes not assumed valid | No geographic code in elite, citizen or admin file |
| Leave-one-cohort-out | All 17 survey signs retained; full coefficient and original-inference p ranges recorded | `leave_one_month_out.csv`, `leaveout_ranges.csv` |
| Missingness | Treatment, cohort/year, quota and Maratha indicator cross-tabs/tests; [0,1] worst-case land bounds | `land-missingness*.csv`, `land-bounds.csv` |
| Missingness by geography/full caste | Unavailable: no geography and no detailed president jati variable; Maratha indicator is the released caste proxy | Dictionary and schema |
| Citizen categorical dependence | Two paired binary partitions and residual reconstructed; full original categories unavailable | `citizen-categories.csv` |
| Citizen sampling/weighting | Informant sampling documented; 1–10 records/GP, usually six; equal-GP weighting sensitivity | `citizens-per-gp.csv`, `citizen-equal-gp-weight.csv` |
| Rich-landowner reporter change | Question/source verified; reporting bias and inside/outside relocation are plausible, unseparated mechanisms | No independent reporter validation or elected-landowner-status variable |
| Unopposed selection | Wording/stage ambiguity verified; aggregate gap persists across indirect cohorts | Exact coding rule not reconstructable from nomination records; none deposited |

## Statistical audit tiers

| Tier / check | Finding or scope limit |
|---|---|
| 1: Denominators and units | One small Figure 3 group-mean SE bug; headline denominators correct. Shares versus differences and planned tenure versus filed events distinguished. |
| 1: Missing coded zero | No fill-to-zero in the released headline estimation; cannot verify unpublished raw observational recoding. Admin missing treatment/outcome is excluded, not converted to no resignation. |
| 1: Row loss | Unique 604-GP key; 3,658 citizen rows preserved in many-to-one join, treatment agrees for every row; admin exclusion counts reconciled. |
| 1: Provenance and consistency | Deposited numerical cells and main labels match rerun; note is generated from outputs. LaTeX-manuscript provenance parser inapplicable: no manuscript TeX deposited. |
| 2: EDA | Mechanical sweeps retained for all three observational inputs; bounded outcomes checked; approximate speech shares inspected. Skewed covariates do not invalidate binary/raw mean arithmetic. |
| 2: Construction and estimand | Survey outcomes are constructed proxies; informal/future turnover distinguished from events; purposive respondent-weighted and GP-weighted estimands separated. |
| 2: Inference | Original HC2/GP-CR2 verified; month dependence changes precision. Independent `clubSandwich` agreement checks CR2 calculations. |
| 2: Multiplicity | No familywise-confirmatory claim made; all 17 survey outcomes reported. No new selective significance filtering or correction family chosen after inspecting results. |
| 3: Design and measurement | Large baseline/cohort differences, land missingness and quota heterogeneity shown. Instrument wording and external-validity restrictions checked. Treatment deployment not randomized in observational component. |
| 3: Experimental branches | Raw experiment cleaning byte-identical and main adjusted effects reproduced. Vignette assignment is distinct from observational electoral reform; no claimed real-world mediation test. |
| 3: Simulation / power | No bespoke causal estimator or power calculation introduced. Analytic HC2 and independent CR2 comparisons validate the variance implementation; no synthetic validation substitutes for missing historical data. |
| 4: Identification/support | Complete treatment separation by month and sparse annual overlap verified; clustering cannot remove cohort confounding. |
| 4: Other econometric designs | This audit does not reinterpret the cross-section as a panel/DiD/IV design. Authors' appendix models run unchanged; new panel dynamics, IV assumptions and structural welfare models are inapplicable. |

## Paper-claim checks

Component outcomes and paired categories were traced separately; no new composite index was built. Baselines, parity reference and heterogeneous quota levels were examined. Reform dose response is inapplicable to binary regime status; election-time plots show the relevant available timing. Mechanism claims were compared with exact questions and the author's own concessions. The analysis distinguishes vignette judgments, stated plans, observed discussion estimates and filed administrative events. Geographic/sampling restrictions accompany conclusions. No population or treatment-on-treated extrapolation was made. An external equal-third institutional norm is not established. Robustness results and null/borderline results are retained rather than selected for a preferred verdict.

Rejected or narrowed criticisms include: parity disproves a relative authority gain; two citizen categories are exact complements; all resignations lack qualitative validation; direct councils necessarily have shorter administrative exposure; annual FE supplies a well-supported corrected effect; and every inferential sensitivity erases the authority result. See `measurement-review.md` and `inference.md` for evidence.

## Data needed to finish the unavailable checks

An anonymized extension can supply district/taluka IDs, verified council term-start and interview dates, original tenure-response categories, meeting attendance/full actor responses, citizen multinomial categories, and administrative event/censor dates without disclosing village names. Raw-to-analysis cleaning code would permit a literal coding audit. Candidate and nomination records are needed to resolve which selection stage “unopposed” describes. None of these records has been requested from third parties.
