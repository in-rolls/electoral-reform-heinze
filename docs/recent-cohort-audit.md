# What survives when older election cohorts are removed?

**The timing concern is severe for reported shared tenure. Several other associations
survive.** Removing early indirect councils reduces the president-reported gap by
66.7% and the citizen-reported gap by 78.1%.
Removing older direct councils as well weakens perceived influence substantially.
Speaking share, unopposed selection and citizen-reported event leadership remain different
in the recent comparisons, though precision depends on the inference method.

These are empirical restrictions on the same deposited data, not theoretical objections.
All 17 survey outcomes and all specified restrictions are retained below. See the
[decision record](recent-cohort-protocol.md) and [complete output](../results/recent/estimates.csv).

## 1. The high early rates are real summaries of the deposited variables

| Outcome | Early indirect | All direct | Later indirect |
|---|---:|---:|---:|
| President reports shared tenure | 41.77% (66/158) | 2.59% (6/232) | 9.48% (20/211) |
| Citizen reports shared tenure | 39.03% (372/953) | 3.00% (42/1399) | 6.93% (85/1226) |
| President unopposed | 43.40% (69/159) | 12.82% (30/234) | 39.05% (82/210) |

“Early indirect” follows the author's definition and includes five early-2017 councils;
it is not literally all pre-2017. Later indirect means election year 2020 or 2021.
Citizen denominators count purposive informants, not independent councils.

The president's early shared-tenure rate is not an estimate based on a few observations:
63 of the positive early reports come from the
142 councils elected in 2015 alone. Their rate is
44.37% (63/142).
Both shared tenure and unopposed selection happen to have 63 positive observations in
2015, but they are not duplicate variables: 27 councils report shared tenure without
unopposed selection and 27 the reverse. [Yearly counts](../results/recent/yearly-counts.csv)
and [early cross-tab](../results/recent/early-cross-tab.csv).

The [survey item](variable-dictionary.md) includes **past or planned tenure sharing**. Consequently,
41.8% is not evidence that 41.8% of the interviewed presidents had already resigned.
The counts establish neither fabrication nor substantive validity of every response.
Raw construction files and the separate response categories remain unavailable.

The within-indirect decline is about 32 percentage points for both tenure measures, while
unopposed selection remains near 40%. That is a specific timing/measurement problem for
shared tenure, not a general collapse of every early-indirect outcome. President speaking
and influence levels also barely differ between early and late indirect councils; the
weaker influence result below arises when older *direct* councils are removed.

## 2. “Latest period” has several meanings, with very different support

| Restriction | Councils, indirect / direct | Election-month clusters, indirect / direct |
|---|---:|---:|
| All direct + later indirect | 211 / 234 | 5 / 26 |
| Elections 2018 onward, both arms | 211 / 86 | 5 / 21 |
| Elections 2019 onward, both arms | 211 / 27 | 5 / 9 |
| Elections 2020 onward, both arms | 211 / 1 | 5 / 1 |
| Elections 2021 onward, both arms | 203 / 0 | 3 / 0 |

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
| President reports shared tenure | -20.72 | -6.89 | -5.95 | -2.07 |
| Citizen reports shared tenure | -17.97 | -3.93 | -4.61 | -3.21 |
| President most influential | 15.07 | 15.37 | 5.72 | 4.69 |
| President speaking share | 5.20 | 5.13 | 5.17 | 6.10 |
| President unopposed | -28.10 | -26.23 | -21.61 | -27.94 |
| Citizen says president leads events | 13.17 | 15.56 | 15.53 | 17.16 |
| President reports landowner influence | -8.29 | -5.67 | -6.86 | -10.48 |

With all direct councils retained, president shared tenure falls from a 20.72-point pooled
gap to 6.89 points. That smaller contrast remains
distinguishable from zero under the original, month-CR2 and wild-bootstrap conventions.
Citizen shared tenure falls to 3.93 points;
its inference is method-sensitive (month CR2 p=0.0537,
wild p=0.0150).

With both arms restricted to 2019 onward, president shared tenure is
7.41% versus 9.48%,
a difference of -2.07 pp with month-CR2 95% CI
[-14.39, 10.25].
Perceived influence differs by 4.69 pp,
CI [-15.36, 24.73].
Both estimates shrink and become imprecise; neither proves zero effect.

Speaking share stays positive at 6.10 pp. Its original HC2
p-value is 0.0508, versus
0.0139 with month CR2 and
0.0256 with the bootstrap. Thus it is not uniformly below .05
under every convention. Unopposed selection and citizen-reported event leadership remain
clearer across these conventions. Landowner influence reports also fall, but none of the
27 recent direct presidents reports influence; that small zero cell deserves care.

The caste-land difference becomes larger, not smaller, under the recent restriction:
24.70 pp. But only 18 direct councils have the measure,
with 6 direct election-month clusters. Its month-CR2 p-value is
0.0254, versus bootstrap p=0.1025.
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

### All direct + later indirect

| Outcome | Observed N, indirect / direct | Means %, indirect / direct | Direct minus indirect [month CR2 95% CI], pp | Original-method p | Month CR2 p | Wild p |
|---|---:|---:|---:|---:|---:|---:|
| President most influential | 211 / 234 | 17.54 / 32.91 | 15.37 [1.69, 29.06] | 0.0002 | 0.0360 | 0.0546 |
| President speaking share | 211 / 234 | 25.93 / 31.06 | 5.13 [0.23, 10.02] | 0.0005 | 0.0440 | 0.0132 |
| President says they decide | 210 / 234 | 24.76 / 32.48 | 7.72 [-6.45, 21.88] | 0.0721 | 0.1997 | 0.2730 |
| Maratha president | 211 / 233 | 18.96 / 33.05 | 14.09 [0.24, 27.94] | 0.0007 | 0.0477 | 0.0333 |
| President caste's estimated land share | 209 / 167 | 28.86 / 44.29 | 15.43 [8.58, 22.29] | <.0001 | 0.0027 | 0.0004 |
| Male president | 211 / 234 | 38.86 / 51.71 | 12.85 [-6.27, 31.97] | 0.0064 | 0.1326 | 0.1460 |
| President owns/plans to inherit land | 210 / 231 | 34.29 / 48.92 | 14.63 [-1.02, 30.28] | 0.0018 | 0.0600 | 0.0398 |
| Household large vehicle | 211 / 234 | 18.96 / 28.63 | 9.68 [-3.15, 22.50] | 0.0163 | 0.1025 | 0.1154 |
| Pacca dwelling | 211 / 234 | 53.08 / 61.54 | 8.46 [-21.63, 38.55] | 0.0721 | 0.4703 | 0.5770 |
| President unopposed | 210 / 234 | 39.05 / 12.82 | -26.23 [-35.77, -16.69] | <.0001 | 0.0019 | 0.0002 |
| President reports shared tenure | 211 / 232 | 9.48 / 2.59 | -6.89 [-10.58, -3.20] | 0.0026 | 0.0071 | 0.0082 |
| President reports landowner influence | 210 / 229 | 10.48 / 4.80 | -5.67 [-13.27, 1.93] | 0.0265 | 0.1052 | 0.1299 |
| Citizen nominates president to bureaucrat | 1253 / 1395 | 59.22 / 66.45 | 7.23 [-5.01, 19.48] | 0.0032 | 0.1716 | 0.2663 |
| Citizen says president leads events | 1240 / 1363 | 59.27 / 74.83 | 15.56 [0.46, 30.66] | <.0001 | 0.0460 | 0.0082 |
| Citizen nominates outsider to bureaucrat | 1253 / 1395 | 14.92 / 11.54 | -3.38 [-8.88, 2.12] | 0.0278 | 0.1586 | 0.2843 |
| Citizen says former/other leads events | 1240 / 1363 | 20.56 / 14.75 | -5.82 [-16.46, 4.82] | 0.0013 | 0.1989 | 0.2808 |
| Citizen reports shared tenure | 1226 / 1399 | 6.93 / 3.00 | -3.93 [-7.97, 0.11] | 0.0073 | 0.0537 | 0.0150 |

### Elections 2018 onward, both arms

| Outcome | Observed N, indirect / direct | Means %, indirect / direct | Direct minus indirect [month CR2 95% CI], pp | Original-method p | Month CR2 p | Wild p |
|---|---:|---:|---:|---:|---:|---:|
| President most influential | 211 / 86 | 17.54 / 23.26 | 5.72 [-3.75, 15.19] | 0.2796 | 0.2034 | 0.1880 |
| President speaking share | 211 / 86 | 25.93 / 31.10 | 5.17 [0.35, 9.99] | 0.0106 | 0.0383 | 0.0258 |
| President says they decide | 210 / 86 | 24.76 / 33.72 | 8.96 [-5.84, 23.76] | 0.1322 | 0.2027 | 0.2018 |
| Maratha president | 211 / 86 | 18.96 / 37.21 | 18.25 [2.53, 33.97] | 0.0022 | 0.0277 | 0.0128 |
| President caste's estimated land share | 209 / 58 | 28.86 / 47.30 | 18.44 [9.31, 27.57] | <.0001 | 0.0013 | 0.0002 |
| Male president | 211 / 86 | 38.86 / 48.84 | 9.97 [-7.86, 27.81] | 0.1190 | 0.2359 | 0.2308 |
| President owns/plans to inherit land | 210 / 84 | 34.29 / 46.43 | 12.14 [-6.90, 31.18] | 0.0581 | 0.1820 | 0.1826 |
| Household large vehicle | 211 / 86 | 18.96 / 29.07 | 10.11 [-3.93, 24.16] | 0.0729 | 0.1369 | 0.1534 |
| Pacca dwelling | 211 / 86 | 53.08 / 65.12 | 12.04 [-15.04, 39.11] | 0.0536 | 0.3388 | 0.3391 |
| President unopposed | 210 / 86 | 39.05 / 17.44 | -21.61 [-31.01, -12.20] | <.0001 | 0.0006 | 0.0007 |
| President reports shared tenure | 211 / 85 | 9.48 / 3.53 | -5.95 [-10.68, -1.22] | 0.0379 | 0.0194 | 0.0172 |
| President reports landowner influence | 210 / 83 | 10.48 / 3.61 | -6.86 [-13.15, -0.58] | 0.0209 | 0.0357 | 0.0290 |
| Citizen nominates president to bureaucrat | 1253 / 513 | 59.22 / 65.89 | 6.67 [-6.17, 19.51] | 0.0356 | 0.2680 | 0.2682 |
| Citizen says president leads events | 1240 / 504 | 59.27 / 74.80 | 15.53 [2.98, 28.08] | <.0001 | 0.0210 | 0.0131 |
| Citizen nominates outsider to bureaucrat | 1253 / 513 | 14.92 / 10.33 | -4.59 [-10.36, 1.17] | 0.0208 | 0.1042 | 0.1156 |
| Citizen says former/other leads events | 1240 / 504 | 20.56 / 16.67 | -3.90 [-13.34, 5.54] | 0.0973 | 0.3722 | 0.3939 |
| Citizen reports shared tenure | 1226 / 517 | 6.93 / 2.32 | -4.61 [-8.18, -1.04] | 0.0032 | 0.0174 | 0.0208 |

### Elections 2019 onward, both arms

| Outcome | Observed N, indirect / direct | Means %, indirect / direct | Direct minus indirect [month CR2 95% CI], pp | Original-method p | Month CR2 p | Wild p |
|---|---:|---:|---:|---:|---:|---:|
| President most influential | 211 / 27 | 17.54 / 22.22 | 4.69 [-15.36, 24.73] | 0.5848 | 0.5757 | 0.5455 |
| President speaking share | 211 / 27 | 25.93 / 32.04 | 6.10 [1.85, 10.35] | 0.0508 | 0.0139 | 0.0256 |
| President says they decide | 210 / 27 | 24.76 / 29.63 | 4.87 [-32.50, 42.23] | 0.6066 | 0.7525 | 0.8183 |
| Maratha president | 211 / 27 | 18.96 / 40.74 | 21.78 [-10.25, 53.82] | 0.0305 | 0.1417 | 0.1153 |
| President caste's estimated land share | 209 / 18 | 28.86 / 53.56 | 24.70 [5.47, 43.93] | 0.0019 | 0.0254 | 0.1025 |
| Male president | 211 / 27 | 38.86 / 55.56 | 16.69 [-4.70, 38.09] | 0.1067 | 0.1017 | 0.0601 |
| President owns/plans to inherit land | 210 / 27 | 34.29 / 48.15 | 13.86 [-14.82, 42.54] | 0.1811 | 0.2707 | 0.2937 |
| Household large vehicle | 211 / 27 | 18.96 / 29.63 | 10.67 [-7.05, 28.40] | 0.2551 | 0.1834 | 0.1142 |
| Pacca dwelling | 211 / 27 | 53.08 / 62.96 | 9.88 [-29.23, 49.00] | 0.3278 | 0.5465 | 0.5304 |
| President unopposed | 210 / 27 | 39.05 / 11.11 | -27.94 [-44.23, -11.65] | <.0001 | 0.0068 | 0.0118 |
| President reports shared tenure | 211 / 27 | 9.48 / 7.41 | -2.07 [-14.39, 10.25] | 0.7078 | 0.6851 | 0.6526 |
| President reports landowner influence | 210 / 27 | 10.48 / 0.00 | -10.48 [-16.09, -4.86] | <.0001 | 0.0048 | 0.0116 |
| Citizen nominates president to bureaucrat | 1253 / 159 | 59.22 / 73.58 | 14.37 [2.30, 26.43] | 0.0024 | 0.0281 | 0.0504 |
| Citizen says president leads events | 1240 / 157 | 59.27 / 76.43 | 17.16 [2.56, 31.76] | <.0001 | 0.0295 | 0.0312 |
| Citizen nominates outsider to bureaucrat | 1253 / 159 | 14.92 / 5.03 | -9.89 [-16.91, -2.88] | <.0001 | 0.0152 | 0.0172 |
| Citizen says former/other leads events | 1240 / 157 | 20.56 / 16.56 | -4.00 [-14.38, 6.37] | 0.1735 | 0.3655 | 0.2798 |
| Citizen reports shared tenure | 1226 / 161 | 6.93 / 3.73 | -3.21 [-10.86, 4.45] | 0.2686 | 0.3308 | 0.2864 |

The empirical conclusion is therefore outcome-specific: the dramatic pooled rotation
gap is heavily dependent on the early indirect cohort; the influential-actor difference
depends substantially on older direct councils; several other reported associations
persist. Missing interview and council-history dates prevent a comparison at equal
term age, and the very latest election years cannot support a two-regime comparison.
