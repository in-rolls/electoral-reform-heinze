# Preregistration and experimental sample audit

The main experimental hypotheses, outcome coding and model specifications match the
preserved analysis plan. The plan explicitly discloses registration after implementation
but before the author received the data. The registration concerns analysis after fieldwork. This audit cannot independently verify when the
author first accessed data or reconstruct unprovided randomization logs.

## Original sources

OSF records registration on **18 October 2024 at 16:26:58 UTC**. The registry response to
the existing-data question is “Registration prior to accessing the data.” Page 2 of the
attached plan describes the same timing. Its planned sample is 2,340 voters. See the
[registration](https://osf.io/a59bu/), [public metadata](../sources/preregistration/registration.json),
and [unchanged analysis plan](../sources/preregistration/analysis-plan.pdf).
The downloaded PDF SHA-256 matches the digest stored in the registration itself.

## Plan-to-code comparison

| Plan | Released implementation | Finding |
|---|---|---|
| Sections 3.2 and 4: four caste/gender conditions; president versus someone else; resign versus resist; likely versus unlikely backlash | Raw `sarpanchgender`, `sarpanchcaste`, `q9.2.1`, `q9.2.3`, `q9.2.4`; `original/code/clean.R` | Main binary mappings agree. Unanswered/unrecognized outcomes remain missing. |
| Section 5: four main contrasts for gender/caste and authority/pliability, two secondary backlash contrasts | `original/code/appendix.R`, Table F.4; main Figure 6 and Appendix H | All six contrasts are reported, unadjusted and adjusted. The S1/S2 labels are reversed in the appendix relative to the plan, but neither secondary test is omitted. |
| Sections 5/5.1: OLS, heteroskedasticity-robust SEs, adjusted preferred models, listed respondent covariates | `lm_robust`, HC2; rural, age, gender, religion, caste, education, prior voting, local knowledge, gender norms | Specifications agree with the stated plan. Both adjusted and unadjusted results remain in the audit. |
| Section 5: exploratory interaction | Appendix F and main discussion | The paper calls the interaction underpowered rather than presenting separate significance as proof of a difference. |
| Section 5: exploratory qualitative reasons for answers | These fields are absent from the released raw CSV | Complete execution of this part cannot be verified. This is an access limit, not evidence it was not done. |

The plan fixes the hypothetical president's age, one year in office, and a Maratha-majority
village. The pilot discussion on p.3 explicitly explains adding majority information after
participants requested population context for interpreting dominance. Consequently,
the caste contrast is a bundled identity/majority-position contrast in that setting, not an
estimate holding numerical group status constant. It is also an experiment on expectations,
not observed administration.

## Sample flow and uncertainty

The [generated diagnostics](diagnostics.md#experiment-reconciliation) reconcile
raw records, assignments, valid responses and covariate-complete observations. All four
assignment cells' missing counts are retained. The main-text N corresponds to valid
authority answers, while the cell counts describe assigned respondents. This is not a
verified sample-size error. Every raw education response maps to the cleaning categories;
the literal “up to 10th grad” in the code matches the actual input.

Outcome nonresponse means the estimated response contrasts are observed-answer contrasts;
causal interpretation for every assigned participant also requires assumptions about the
missing answers. The small recorded losses do not by themselves establish material bias.
The sampling uses selected sites and a random-walk procedure within gender/ethnic targets;
random treatment assignment does not make it a population probability sample.

Table F.3 contains extreme joint HC2 balance tests for two conditions. The
[retained balance diagnostic](diagnostics.md#experimental-balance-sparse-cell-diagnosis)
shows their sensitivity to seven respondents in sparse religion categories with no Maratha
assignments. It also reports realized respondent-gender imbalance across the four conditions.
Thus this audit does not certify that every covariate is balanced or that assignment was
implemented correctly. The prespecified gender adjustment remains in the substantive models,
and the sparse-category respondents are retained. Neither the extreme Wald statistics nor
their sensitivity alone demonstrates randomization failure.

The main quantitative analyses match the registered plan. The substantive limitation is
transport from hypothetical social identity to actual elite capture and institutional mediation.
