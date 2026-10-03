# Follow-up diagnostic decisions

These are exploratory audit checks selected after reviewing the published results and
the first replication. This record precedes execution of `critical_diagnostics.R`; it
is not a preregistration or a claim that the auditors were blind to results.

1. **Sensitivity benchmark.** Recreate every observational model underlying Figures
   D.1–D.3. Export both treatment-side and outcome-side partial R² for the gender quota,
   the author's 1×/2×/3× bounds, and equal-strength robustness values. A benchmark strong
   on both dimensions would strengthen the paper's defense. A weak treatment association
   or near-zero outcome association would limit the substantive reassurance. Do not
   choose alternative benchmarks to obtain a preferred result. These are the author's
   ordinary linear-model calculations; they do not inherit the main models' robust or
   clustered uncertainty.
2. **SC-reserved authority.** Reproduce the five authority differences within SC-reserved
   councils, with their actual denominators, then directly test treatment-by-SC-reservation
   interactions using HC2 for council outcomes and GP CR2 for citizen outcomes. Positive
   effects within these seats would limit any claim that selecting Maratha presidents is
   necessary for greater authority. They would not exclude class-based selection, identify
   a mediation effect, or establish that quotas change the treatment effect. Report every
   outcome and every interaction, regardless of significance.
3. **Experiment sample flow.** Reconcile raw records, assigned conditions, valid outcomes,
   and covariate-complete samples with the paper's stated N. Count missing outcomes by
   assignment and reproduce all six unadjusted/adjusted main contrasts. A reconciled
   count is a rejected error allegation; an unexplained loss remains unresolved. Missing
   responses are not coded as failures. Do not substitute a new estimator for the author's
   prespecified comparisons.

No diagnostic can recover missing interview dates, anonymized geography, predecessor
identities, policy beneficiaries, or raw observational construction. Those limitations
require data, not additional specifications. Existing election-month inference and
leaveout results are retained without rerunning a search for significant or null results.

## Later addition: experimental balance

During final review, Table F.3's large joint HC2 F statistics alongside small R² prompted
a further arithmetic check. Read-only investigation identified seven respondents in two
sparse religion categories, all assigned to Kamble conditions. The retained diagnostic
reports all four assignment regressions with original HC2, ordinary F tests, and HC2 after
excluding those seven solely to localize the statistic. It also retains the respondent-
gender contingency imbalance. These checks were selected after seeing the anomaly, not
prespecified. Substantive experimental models retain all eligible respondents and the
original adjustment. Disappearance of the extreme Wald statistic localizes sensitivity;
it does not establish balance on all covariates or verify correct randomization.
