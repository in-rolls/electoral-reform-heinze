# Election-cohort restriction diagnostic

This follow-up addresses the user's concern about high early-indirect shared-tenure rates.
Existing transition estimates and initial raw tabulations were inspected before specifying
these comparisons. This is exploratory sensitivity analysis, not a preregistration.

- **Drop early indirect:** retain all direct councils and indirect councils elected in 2020
  or later. This reproduces the paper's second-transition contrast, not a wholly recent sample.
- **2018 onward:** require the recorded incumbent election year to be at least 2018 for both
  arms. This removes the large 2017 direct cohort as well as all early indirect observations.
- **2019 onward:** retain the last full calendar year of direct elections and later cohorts.
  This brings the comparison closer in calendar time but leaves few direct councils.
- **2020 onward / 2021 onward:** report support and means. Do not report regression inference
  when either arm has fewer than two observed councils. Citizen rows cannot manufacture
  independent support where only one direct council remains.

Retain all 17 survey outcomes for every supported comparison, including results that remain
positive or become stronger. Report observed counts, raw means, original-convention HC2/GP
CR2 uncertainty, election-month CR2 uncertainty, and the same null-imposed wild bootstrap
used in the earlier audit (9,999 Rademacher draws, seed 20261003). Show cluster counts by
arm and effective degrees of freedom. There are only five later-indirect election months,
with substantial concentration; bootstrap agreement is a sensitivity result, not assurance
that inference or causal identification is solved.

Also recover yearly counts and the early president shared-tenure/unopposed cross-tab to
check whether the high rates reflect arithmetic mistakes, tiny denominators or duplicated
binary vectors. Unavailable raw construction and interview dates limit the conclusion.
Do not label a high rate impossible simply because it is surprising.

These restrictions concern election dates, not interview waves or equal time at risk.
Administrative resignation data have no election dates and cannot be included. The author's
early-indirect definition includes five councils elected in early 2017; the report will use
“early indirect,” rather than presenting it as literally all pre-2017.
