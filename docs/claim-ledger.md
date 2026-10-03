# Claim-to-evidence ledger

This ledger adjudicates the published argument, not the author's intentions. “Insufficiently
established” means the evidence does not identify the stated claim; it does not mean the
opposite has been demonstrated. Printed page numbers refer to the preserved
[paper](../sources/paper.pdf) and [appendix](../sources/appendix.pdf).

The observational estimand is a direct-minus-indirect difference across the sampled councils
or respondents, interpreted causally under the assignment and measurement assumptions.
Council outcomes weight observed councils equally; citizen outcomes weight observed
informants equally, with GP-clustered original inference. Survey interviews span 2020–22.
The administrative estimand is a cumulative term-level event indicator in one district.
The experimental estimand is the effect of assigned hypothetical caste/gender descriptions
on respondent predictions. It does not estimate an electoral-reform effect.

| Claim and published location | Evidence and producing variables | Strongest challenge | Author's defense and audit adjudication |
|---|---|---|---|
| Direct elections increase de facto authority. Abstract; pp.9, 12–13; Figure 4. | `prop_speakingtime_sarpanch`, `most_influential_gd`, `i_decide_masik_sabha`, `sarpanch_nominate_BDO`, `sarpanch_inauguralevents`; `original/code/main.R`, Figure 4 block. [Raw means](../results/audit/raw-means.csv). | Regime, historical cohort, experience and interview timing are not separately observed; discussion behavior does not cover all governing power. | Historically staggered scheduling, covariate balance, several reporters and positive comparisons support the argument. **Supported with narrower scope:** higher measured authority; causal attribution remains conditional. Near-parity does not refute the comparative gain. |
| Electoral timing gives plausibly quasi-experimental assignment. pp.7–9; Appendix C. | Historical interviews; establishment dates; Tables C.1–C.5; `sarpanch_election_year/month`, `establishment_year`; `appendix.R` C blocks. | Evidence against manipulation does not separate time at risk or term age from regime. The recorded date can refer to the current incumbent. | Unexpected reforms and administrative discretion make village self-selection less plausible. Joint and prognosis-weighted balance checks provide real but partial reassurance. **Conditional:** assignment story is credible enough to assess, not proved by balance; missing temporal records are decisive. |
| Election type determines whether executive succession is village-wide or internal. pp.5–6; Table 1. | Institutional narrative, `direct`, shared tenure and administrative `resigned`. [Official-law comparison](institutions.md#follow-up-audit-powers-and-succession). | The 2020 amendment changes the ordinary replacement route for directly elected presidencies; reform also changes executive powers and removal rules. | The earlier direct-successor rule supports the original theory. The paper mentions centralized powers generally. **Verified institutional qualification:** the categorical succession account omits a change relevant during follow-up. No council-level miscoding or numerical correction is established. |
| Direct elections increase formal capture. pp.2, 13; Figure 5 upper panel. | `sarpanch_maratha`, `sarpanch_male`, `avg_prop_land_held_sarpanch_caste`, `sarpanch_land_own_name`, `three_four_wheeler`, `pacca_house`; `main.R` Figure 5. | Identity and assets do not directly measure control for elite ends. Land measurement and missingness limit coverage. | Local history and case evidence link privilege to power; footnote 33 acknowledges bundled attributes. **Supported with narrower scope:** more socially/asset-advantaged officeholders; large-sample capture is not directly established. |
| Direct elections decrease informal capture. pp.13–15; Figure 5 lower panel. | `sarpanch_uncontested`, `resignation`, `rich_landowner_influences_gp`, citizen outsider categories and rotation reports, administrative `resigned`. [Dictionary](variable-dictionary.md). | Planned rotation, selection-stage comparability, treatment-dependent reporters and administrative exposure do not identify a common capture construct. | Qualitative cases and follow-up attribution validate some elite tactics; the paper discusses an alternative explanation for unopposed elections. **Supported with narrower scope:** several reports and cumulative event rates are lower; total or exposure-adjusted capture is not identified. |
| Robustness across both policy transitions supports the result. Appendix D.1.2/D.2.2, Tables D.2/D.9/D.10. | Same direct cohort compared to early or late indirect councils; [transition contrasts](../results/audit/transition-contrasts.csv). | Comparisons share treated observations; indirect shared-tenure levels differ greatly; early land observations are exceptionally scarce. | Both contrasts often have the predicted sign. **Qualified support:** this is useful comparison sensitivity, not independent replication or within-council change. |
| Omitted confounders would have to exceed an implausible multiple of quota strength. p.8; Appendix D.1.5/D.2.5. | `sensemakr` with `reserved_women`, `kd=ky=1:3`, ordinary `lm`; `appendix.R` Figures D.1–D.3. [All calibrated bounds](../results/critical/sensitivity-bounds.csv). | The quota weakly predicts treatment; for some capture outcomes it barely predicts the outcome either. Ordinary sensitivity t-values differ from the main robust/clustered framework. | Strong gender effects on some authority measures make the benchmark substantively relevant on that dimension. **Interpretive overreach:** correct arithmetic does not justify the blanket plausibility claim. See [full diagnostic](critical-diagnostics.md). |
| Formal capture causes an authority advantage. pp.2, 9–10, 15–16; Figure 6. | Randomized hypothetical `Male` and `Maratha`; `authority`, `pliability`; `clean.R`, `main.R` Figure 6, `appendix.R` Table F.4. | Identity in a fixed majority-caste village changes expectations; actual capture, election rules and governing behavior are not randomized. | The paper explicitly calls this a partial mechanism test and disclaims causal mediation (footnote 44). **Supported with narrower scope:** causal effects of described identity on vignette responses; not realized institutional mediation. |
| Established elites adapt by shifting from proxies to officeholding. pp.10–11; Appendix E. | Named/pseudonymized family histories, interviews, observations and specific village decisions; no released population-wide predecessor/network variable. | Selected matched cases do not identify representative transition rates or exclude alternative pathways in the survey sample. | Dynastic continuity and explicit prior proxy arrangements are direct process evidence, beyond demographic resemblance. **Supported in selected cases; prevalence and average mechanism contribution unresolved.** |
| The case demonstrates elite invariance and hard limits to democratic deepening. pp.2, 17. | Combination of authority, officeholder composition, informal proxies and case studies. No comparable quantitative measure of continuing control, accountability or beneficiaries across regimes. | Different proxy changes cannot establish continued elite control of decisions or rule out gains in accountability or marginalized participation; an exact scalar offset is not required. | Cases show persistent coercion and exclusion; theory offers a coherent account. **Insufficiently established at sample level:** persistence is plausible and locally documented, not identified as the reform's general result. |
| SC quotas combined with direct elections may offer a way out. p.17; Appendix H. | SC-reserved subgroup, `reserved_sc`; authority/capture measures and backlash vignette. [Direct interaction tests](../results/critical/sc-authority.csv). | Within-SC authority gains do not show amplification by quotas; class privilege can remain and capture proxies give mixed results. | Author labels the evidence suggestive and underpowered; case studies show empowerment as well as threats. **Plausible scope condition, not established escape from total elite control.** |
| The vignette follows a preregistered design. pp.2, 9, 16; Appendix F. | [OSF plan and code comparison](preregistration-review.md); registration, raw assignment fields, cleaning, six main contrasts. | Registration occurs after collection; exploratory qualitative answers and assignment logs are not released. | Plan explicitly discloses registration before data access; main coding and models agree. Counts reconcile. **Main quantitative correspondence verified; complete implementation compliance and data-access history not independently verifiable.** |

## Rival accounts and discriminating evidence

| Rival explanation | What would discriminate it from the paper's mechanism? | Current adjudication |
|---|---|---|
| Legal powers or a broader mandate increase presidential authority. | Linked legal exposure and interview dates; direct evidence on agenda control and decision implementation; comparisons holding formal powers fixed. | Compatible with the authority differences and incomplete statutory comparison; contribution not estimated. |
| Term age or changing rotation norms affect shared tenure. | Original term starts, interview dates, planned/completed rotation categories, event histories; compare equal exposure where supported. | Large indirect-cohort differences motivate the check. No exposure-adjusted effect is available. |
| Broader elections select advantaged candidates through voter preferences or campaign resources without preserving total capture. | Candidate pools, nomination histories, voter choice and accountability, decision beneficiaries, matched elite-family histories. | Compatible with the six composition indicators. Qualitative cases show coercive capture in some settings but do not eliminate this account generally. |
| Reporting changes with who becomes president. | Same independently sampled reporters over time; separate outside/elected landowners; direct decisions or network validation. | Plausible for president self-reports; not demonstrated reporting bias. |
| The exact elite-adaptation process is common and preserves control. | Pre/post elite network continuity, representative process evidence, stable or worsening elite control over comparable decisions and benefits. | Locally documented; the required sample-wide evidence is absent. |

## Criticisms rejected or narrowed

- Near-one-third authority levels do not contradict an increase; the paper explicitly says
  direct presidents are not autocrats. Equal thirds is not an established substantive null.
- The citizen paired categories are not exact complements; residual categories matter.
- The absence of a month-FE coefficient does not prove historical assignment is endogenous.
- Year fixed effects do not supply a well-supported corrected estimate.
- Direct councils are not shown to have shorter administrative exposure; the likely ordering
  under some timelines is the opposite.
- The paper contains actual elite-adaptation histories and validation of some rotation tactics.
- The experimental denominators reconcile; disclosed post-collection/pre-access registration
  is not evidence of outcome-driven analysis.
- Gender-quota sensitivity calculations reproduce. The flaw is the breadth of their interpretation,
  not arithmetic failure. Infinite boundary t-values are not observed infinite precision.

## Minor reporting issue, kept in proportion

The published Appendix Table C.1 note (p.24) reverses the regression direction: it describes
establishment year on current election year, whereas the coefficient labels and author code
fit `sarpanch_election_year ~ establishment_year`. The deposited table note is already correct.
The coefficient .018, SE .005 and N=576 reproduce. This is a verified published-caption
mismatch, not a number-changing defect or a reason to reject the historical argument.
