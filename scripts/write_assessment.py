"""Build the claim assessment and diagnostic tables from audit outputs."""

from report_utils import ROOT, pct, rows


def main():
    means = {r["variable"]: r for r in rows("results/audit/raw-means.csv")}
    benchmarks = {
        r["variable"]: r for r in rows("results/critical/sensitivity-benchmarks.csv")
    }
    bounds = {
        (r["variable"], r["bound_label"]): r
        for r in rows("results/critical/sensitivity-bounds.csv")
    }
    quota = {
        (r["variable"], r["comparison"]): r
        for r in rows("results/critical/sc-authority.csv")
    }
    experiment = {
        (r["variable"], r["treatment"], r["adjusted"]): r
        for r in rows("results/critical/experiment-estimates.csv")
    }
    flow = {
        r["stage"]: int(r["n"]) for r in rows("results/critical/experiment-flow.csv")
    }
    balance = {
        (r["condition"], r["specification"]): r
        for r in rows("results/critical/experiment-balance.csv")
    }
    gender_balance = rows("results/critical/experiment-gender-balance.csv")[0]
    cohorts = {
        (r["variable"], r["period"]): r for r in rows("results/audit/cohort-means.csv")
    }
    speech = means["prop_speakingtime_sarpanch"]
    influence = means["most_influential_gd"]
    housing = bounds["pacca_house", "3x reserved_women"]
    rotation = bounds["resignation", "3x reserved_women"]
    speech_bound = bounds["prop_speakingtime_sarpanch", "3x reserved_women"]
    experiment_male = experiment["authority", "Male", "TRUE"]
    experiment_caste = experiment["authority", "Maratha", "TRUE"]
    sc_influence = quota["most_influential_gd", "sc_1"]
    sc_speech = quota["prop_speakingtime_sarpanch", "sc_1"]
    sc_influence_interaction = quota["most_influential_gd", "interaction"]
    sc_speech_interaction = quota["prop_speakingtime_sarpanch", "interaction"]
    rotation_levels = ", ".join(
        pct(cohorts["resignation", period]["mean"]) + "%"
        for period in ("early_indirect", "direct", "late_indirect")
    )

    assessment = f"""# Electoral reform: interpretation of the evidence

The study reports differences in presidential participation, officeholder characteristics
and shared tenure across election regimes. Its village histories document elite adaptation
in selected settings, and its vignette measures expectations about hypothetical presidents.
Interpreting these findings together requires distinguishing composition, reported influence,
actual decisions and the timing of institutional changes.

The [numerical results](audit.md), [measurement table](claims.md) and
[diagnostic tables](diagnostics.md) provide the corresponding estimates and definitions.
Diagnostic choices are documented in [methods](methods.md#exploratory-diagnostic-choices).
Page references use the printed pages of the [paper](../sources/paper.pdf) and
[appendix](../sources/appendix.pdf).

## Officeholder composition and elite control

The paper defines capture in terms of elites controlling institutions for their own ends,
excluding marginalized people, and producing outcomes less aligned with those people's
needs (p.3). It then measures formal capture through six president characteristics: caste,
gender, estimated caste land share, land ownership or intended inheritance, a household
vehicle, and dwelling construction (p.13; Figure 5). The published increases reproduce:
Maratha +9.8 pp, male +16.0 pp, and caste land share +15.4 pp, for example. These show who
holds office and their social advantages. They do not directly measure whose interests the
officeholder serves or how residents can constrain that officeholder.

Greater elite representation
and fewer reports of outside interference are compatible with several outcomes: continued
capture, more accountable elite politicians, competition between elite factions, or changes
in the distribution of influence among elites and nonelites. These proxies do not establish
continuing elite control over comparable decisions or beneficiaries across regimes. The joint
pattern is consistent with both persistent capture and more accountable elite
leadership; distinguishing these possibilities requires evidence on decisions and accountability.

The qualitative evidence supplies observations of these processes. The main cases and Appendix E
describe coercion, proxy selection, dynastic continuity, silenced citizens, and concrete
decisions favoring powerful people. In Shelgaon, the direct president comes from the
established ruling family; Appendix E also describes a family that influenced politics
before holding the direct presidency. These cases document established elites adapting.

The seven 2024 comparison councils come from one Pune block, with one initial random
selection and nearby matched cases thereafter (Appendix A, pp.4–5). That is useful for
tracing processes; it does not estimate how often adaptation occurs across the survey sample
or demonstrate persistent control across the sample. Earlier fieldwork is broader, but it does not turn
these matched cases into a representative transition panel. The cases document adaptation
in those settings; its prevalence across the survey population is not estimated.

## Election timing and statutory powers

Election cycles predate the reform,
administrators schedule elections, and the policy changes were reportedly difficult for
villages to anticipate. Published balance diagnostics and historical establishment checks
provide evidence against some forms of strategic selection (pp.7–9; Appendix C).

However, even an as-if-random phase in an electoral cycle assigns both a regime and the
age of the council term at observation. A difference in rotation, accumulated experience,
or succession can therefore arise without strategic sorting. Interview dates are absent
from the release, although the survey spans 2020–22. The election item asks when the
current president was elected, which need not identify the original council term. These
are unseparated channels, not demonstrated estimates of bias.

For shared tenure, the published early indirect, direct and
late indirect percentages, 41.8/2.6/9.5, reproduce as {rotation_levels}.
The same indirect regime has sharply different cohort levels. That does not prove an
exposure explanation, since the question includes future plans. A causal interpretation of the
pooled gap requires accounting
for timing, selection and measurement.
Comparing the same direct cohort with early and late indirect councils does not constitute
two independent replications. Exact-month fixed effects cannot identify a separate regime
coefficient, but that algebra alone does not invalidate a historically justified design.
Year-adjusted estimates rely on sparse overlap and are not corrected effects.

**The institutional treatment is also broader, and changes over time.** The official
2017 reform, enacted as Act LIV of 2018, expressly assigns directly elected presidents
additional agenda, budget and resolution-referral powers, and modifies no-confidence
procedures. The 2020 Act extends comparable agenda and budget provisions generally.
Thus legal powers and experience offer a pathway alongside selection of different
officeholders. These provisions do not prove that legal powers caused the measured
gap; by the survey period some provisions had been generalized. The histories need to be
matched to interviews. The paper mentions a political aim of centralized powers (p.6),
but does not isolate these statutory changes from the method of election.

Table 1 and pp.5–6 describe village-wide
replacement elections after a direct president leaves. That matches the earlier rule,
but section 8 of the 2020 Act provides for replacement from among council members,
subject to protection for vacancy procedures already begun. This qualification matters
to the theory that direct-election succession makes rotation less credible. It also raises
the possibility that a successor is recorded as indirect in a council that began under
the direct regime. The deposited histories cannot quantify that possibility. The observed
regime comparisons combine election method, officeholder selection and changes in statutory
powers and succession rules.
See the [dated statutory comparison](institutions.md#follow-up-audit-powers-and-succession).

## Interpretation of the capture indicators

The indicators differ in wording, respondent and denominator.

- **Shared tenure:** the published 23.3% versus 2.6% refers to past or planned tenure
  sharing, not simply completed resignation. The original categories are unavailable.
  Follow-up attribution of rotation to influential villagers in 71 of 87 interviewed
  positive cases supports the existence of the tactic. It does not validate negative
  reports, resolve exposure, or establish a comparable reporting process across cohorts.
- **Unopposed selection:** the published 40.9% versus 12.8% compares reports arising from
  different electoral institutions, with no recorded nomination stage. A larger electorate
  or different candidate pool can change this rate without a change in capture. The paper
  acknowledges the higher-stakes alternative (p.15; Appendix D.3); voting reports do not
  establish comparable presidential nomination and withdrawal processes.
- **Rich-landowner influence:** the 13.1% versus 4.8% outcome comes from presidents, whose
  selection changes under the proposed mechanism. The questionnaire does not explicitly
  exclude an elected landowner. Reporter change and movement of elites into office are
  plausible explanations, not measured reporting biases. The item cannot independently
  establish how total elite influence changes.
- **Caste land share:** the +15.4 pp result uses a bureaucrat's approximation, with coverage
  of {cohorts['avg_prop_land_held_sarpanch_caste', 'early_indirect']['n']}/159 early indirect,
  {cohorts['avg_prop_land_held_sarpanch_caste', 'direct']['n']}/234 direct, and
  {cohorts['avg_prop_land_held_sarpanch_caste', 'late_indirect']['n']}/211 late indirect
  councils. The late comparison remains positive. The early-transition comparison has limited
  observed support for this measure.
- **Citizen corroboration:** the authority and outsider categories come from two shared
  questions, and citizens are purposively chosen informants. These provide several
  perspectives but fewer independent measurements than the count of coefficients suggests.
  They also measure the fraction of informants giving an answer, not the fraction of actual
  village events at which an officeholder performs a duty. The paper's p.13 footnote 32
  shifts toward the latter interpretation when discussing nonperformance around 40% of
  the time. The survey has no event denominator.

The administrative result is harder evidence of filed events:
{pct(means['resigned']['indirect_mean'])}% versus
{pct(means['resigned']['direct_mean'])}%. Its exposure problem remains unresolved.
Direct councils are not shown to have less time
at risk; their terms
could be older under the reform timeline. The reported differences concern distinct
measures of selection, influence and turnover. Their comparability as measures of capture
depends on the definitions, reporting processes and exposure windows. Exact items,
variables and full arithmetic are in the
[dictionary](data-dictionary.md) and [numerical results](audit.md).

## Sensitivity to omitted confounding

The paper argues that confounders more than three times as strong as the gender quota are
implausible because the quota strongly predicts outcomes (p.8; Appendix D.1.5 and D.2.5).
The calculation bounds **both** the confounder's association with treatment and its
association with the outcome. Strong outcome prediction does not justify a small bound
on treatment prediction. The official
[sensemakr reference](https://carloscinelli.com/sensemakr/reference/sensemakr.html)
defines these as separate inputs.

The original code reproduces. For speaking share, the 3× scenario permits the confounder
to explain {pct(speech_bound['r2dz.x'], 3)}% of residual treatment variation and
{pct(speech_bound['r2yz.dx'], 2)}% of residual outcome variation. The permitted treatment and
outcome associations therefore differ substantially. For the housing indicator, the permitted
outcome association is only
{pct(housing['r2yz.dx'], 5)}%; for shared tenure it is
{pct(rotation['r2yz.dx'], 5)}%. Those scenarios barely change the coefficients because the
quota explains little variation in these particular outcomes. The informativeness of
this benchmark therefore differs across outcomes.

Unbenchmarked equal-strength robustness values supply more informative context. In the
author's ordinary linear models, loss of conventional significance requires explaining
{pct(benchmarks['pacca_house']['rv_qa'])}% of residual treatment and outcome variation for
housing, {pct(benchmarks['prop_speakingtime_sarpanch']['rv_qa'])}% for speaking, and
{pct(benchmarks['resignation']['rv_qa'])}% for shared tenure. These are conditional
sensitivity quantities, not probabilities that confounding exists. The sensitivity to omitted
confounding varies across outcomes.

The sensitivity models use ordinary `lm`, including for citizen outcomes, while the main
citizen estimates use GP-clustered inference. The t-value sensitivity plots therefore do
not directly describe sensitivity of the main clustered tests. The arithmetic reproduces;
its interpretation is conditional on the treatment-side and outcome-side benchmark strengths.
All 17 models and 51 bound scenarios are retained, including a boundary case for male
officeholding; the calculations use the original benchmark throughout.

## Vignette results and institutional mechanisms

The experiment addresses expectations about presidential authority. Respondents see caste
and gender descriptions of a
hypothetical president in a Maratha-majority village. They predict who would make
decisions. The experiment varies neither election rules, elite control, actual governing
behavior, nor policy beneficiaries. Caste identity and membership of the village majority
move together by design; the pilot explicitly motivated this choice.

The published adjusted +4.9 pp male and +13.9 pp Maratha effects reproduce as
{pct(experiment_male['estimate'])} pp (95% CI
{pct(experiment_male['low'])} to {pct(experiment_male['high'])}) and
{pct(experiment_caste['estimate'])} pp
({pct(experiment_caste['low'])} to {pct(experiment_caste['high'])}).
They are meaningful effects on expectations under the specified vignette. The paper
notes that the experiment does not identify causal mediation (p.16,
footnote 44), and that formal capture bundles attributes and uses of power (p.13,
footnote 33). The experimental estimand concerns expectations under the vignette. Connecting it to
real-world capture and adaptation requires additional evidence.

The preregistration checks do not reveal a substantive departure in the main quantitative
analyses. The plan was registered on 18 October 2024, explicitly after implementation but
before the author received data. Its timing is disclosed. The sample also reconciles:
{flow['raw']:,} raw records, {flow['assigned']:,} assigned respondents,
{experiment['authority', 'Male', 'FALSE']['n']} valid authority answers, and
{experiment_male['n']} adjusted observations. The reported sample sizes reconcile.
The preregistered exploratory qualitative follow-up answers are not released, so complete
compliance cannot be verified. [Preserved plan and comparison](registration.md).

The experiment has some realized covariate imbalance. Table F.3's extreme joint
tests are sensitive to seven respondents in sparse religion categories: excluding these
respondents solely as a diagnostic changes the two Maratha-cell HC2 F statistics from
12.792/20.059 to {float(balance['bharti marathe', 'exclude_sparse_HC2']['f']):.3f}/
{float(balance['rohit marathe', 'exclude_sparse_HC2']['f']):.3f}.
There is also realized respondent-gender imbalance across conditions
(Pearson p={float(gender_balance['p']):.5f}). The prespecified adjustment includes gender.
These observations warrant retaining the assignment-verification limitation; they do not
prove failed randomization. No respondents were removed from the substantive estimates.

The SC-reserved results also limit a single-mechanism account. Among
{sc_influence['councils_indirect']} indirect and {sc_influence['councils_direct']} direct
SC-reserved councils, perceived influence rises
{pct(sc_influence['estimate'])} pp (CI {pct(sc_influence['low'])} to
{pct(sc_influence['high'])}), while speaking rises {pct(sc_speech['estimate'])} pp
(CI {pct(sc_speech['low'])} to {pct(sc_speech['high'])}).
Maratha selection cannot explain these within-SC differences, although class selection
and institutional effects remain possible. The treatment-by-SC interactions are not well
distinguished from zero: p={float(sc_influence_interaction['p']):.3f} for influence and
p={float(sc_speech_interaction['p']):.3f} for speaking. Thus these results do not establish
that reservation amplifies the authority effect. Appendix H appropriately calls the
evidence suggestive. The vignette identifies effects on expected authority; the SC
comparisons do not identify mediation or amplification by reservation.

## Observed presidential participation

Presidential voice is greater on the measured outcomes: speaking rises from
{pct(speech['indirect_mean'])}% to {pct(speech['direct_mean'])}%, and the share judged most
influential rises from {pct(influence['indirect_mean'])}% to
{pct(influence['direct_mean'])}%. These differences have positive intervals under the implemented election-month
inference procedures. These levels describe a comparative gain; the paper
distinguishes the measures from absolute executive control. They support greater measured voice,
subject to the observational design for causal attribution, rather than a finding about
all dimensions of governing power.

The sample also has different officeholder characteristics, less reported rotation and
less reported outside influence under direct elections. Clustering changes uncertainty
for some contrasts. Village histories and vignette responses provide distinct kinds of
evidence on adaptation and expected authority.

## Additional data and scope

The scope is also narrower than general claims about decentralized democracy. Appendix G
collects expert predictions and qualitative accounts from other Indian states. Those
accounts support plausibility elsewhere; they do not provide independent treatment-effect
estimates or establish that the Maharashtra pattern generalizes to other institutional
and social settings. The appendix itself describes the evidence as suggestive.

The highest-value extension is an anonymized history linking original council election
dates, interview dates, incumbent succession, applicable legal rules, and administrative
event and censoring dates. It would allow regime comparisons at comparable
exposure and unchanged treatment classification. The exposure bias could favor either account.

To establish adaptation at scale, the study needs linked identities or family/network codes
for pre-reform brokers and post-reform officeholders, together with comparable measures of
who determines decisions and who benefits. Stable elite control on those measures, despite
changed routes to office, would strengthen the invariance claim. Meaningful gains in
accountability or marginalized participation would indicate a different institutional outcome
even if presidents become richer.

Full original survey categories, actor distributions, anonymized district/taluka identifiers,
and the raw-to-analysis cleaning code would resolve important measurement and inference
questions. Representative longitudinal evidence on elite networks, decisions and
beneficiaries would clarify the relationship between these observed differences and
the proposed institutional mechanism.
"""
    (ROOT / "docs/interpretation.md").write_text(assessment)

    sensitivity_table = []
    for variable, result in benchmarks.items():
        bound = bounds[variable, "3x reserved_women"]
        sensitivity_table.append(
            f"| `{variable}` | {result['n']} | "
            f"{pct(result['quota_treatment_partial_r2'], 4)} | "
            f"{pct(result['quota_outcome_partial_r2'], 5)} | "
            f"{pct(bound['r2dz.x'], 4)} | {pct(bound['r2yz.dx'], 5)} | "
            f"{pct(result['rv_qa'])} |"
        )
    quota_table = []
    for variable, label in (
        ("most_influential_gd", "Most influential"),
        ("prop_speakingtime_sarpanch", "Speaking share"),
        ("i_decide_masik_sabha", "Self-reported decision-maker"),
        ("sarpanch_nominate_BDO", "Citizen nominates president"),
        ("sarpanch_inauguralevents", "Citizen reports events leadership"),
    ):
        q = quota[variable, "sc_1"]
        interaction = quota[variable, "interaction"]
        quota_table.append(
            f"| {label} | {q['n_indirect']} / {q['n_direct']} | "
            f"{pct(q['estimate'])} [{pct(q['low'])}, {pct(q['high'])}] | "
            f"{pct(interaction['estimate'])} "
            f"[{pct(interaction['low'])}, {pct(interaction['high'])}] | "
            f"{float(interaction['p']):.3f} |"
        )
    experiment_table = []
    for outcome in ("authority", "pliability", "backlash"):
        for treatment in ("Male", "Maratha"):
            result = experiment[outcome, treatment, "TRUE"]
            raw = experiment[outcome, treatment, "FALSE"]
            experiment_table.append(
                f"| {outcome} / {treatment} | {raw['n']} / {result['n']} | "
                f"{pct(raw['estimate'])} | {pct(result['estimate'])} "
                f"[{pct(result['low'])}, {pct(result['high'])}] |"
            )
    balance_table = []
    for condition in sorted({key[0] for key in balance}):
        original = balance[condition, "original_HC2"]
        ordinary = balance[condition, "ordinary_F"]
        sparse = balance[condition, "exclude_sparse_HC2"]
        balance_table.append(
            f"| {condition} | {float(original['f']):.3f} / "
            f"{float(original['p']):.3g} | {float(ordinary['p']):.3f} | "
            f"{float(sparse['f']):.3f} / {float(sparse['p']):.3f} |"
        )
    sensitivity_header = (
        "| Outcome | N | Quota: treatment R², % | Quota: outcome R², % | "
        "3× bound: treatment R², % | 3× bound: outcome R², % | RV for significance, % |"
    )
    quota_header = (
        "| Outcome | SC observed N, indirect / direct | Within-SC difference [95% CI], pp | "
        "SC minus non-SC effect [95% CI], pp | Interaction p |"
    )
    diagnostics = f"""# Follow-up numerical diagnostics

Generated by `scripts/write_assessment.py` from `scripts/critical_diagnostics.R`.
The [decision record](methods.md#exploratory-diagnostic-choices) states how each result bears on the
claim. Source observational files remain unchanged.

## Sensitivity calibration

All R² entries below are **percent of residual variance**, not proportions. RV is the
equal-strength robustness value for loss of conventional significance at alpha=.05 in
the author's ordinary linear model. It is not an estimate of actual confounding or a
cluster-robust sensitivity result. Exact baseline estimates, ordinary SEs, robustness
values for reducing estimates to zero, and all bound-adjusted estimates and CIs are in
[benchmarks](../results/critical/sensitivity-benchmarks.csv) and
[bounds](../results/critical/sensitivity-bounds.csv).

{sensitivity_header}
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(sensitivity_table)}

The 3× bounds are sensemakr's benchmark transformations; they need not equal exactly
three times the partial R² in the preceding columns. Every model and all 51 bounds match
execution of the [original author blocks](../results/critical/author-sensitivity-validation.txt).
Partial R² also agrees independently between residual-sum-of-squares and t-statistic
calculations. The [official documentation](https://carloscinelli.com/sensemakr/reference/sensemakr.html)
defines the two association bounds.

For `sarpanch_male`, the quota's outcome association is so strong that the package caps
all three implied outcome bounds at 1. The resulting adjusted SE is zero and t-value
infinite at that mathematical boundary. The warnings and `outcome_bound_at_limit` flag
are retained. This degenerate scenario is not empirical evidence of infinite robustness.
It is also not an error in the observed male-presidency coefficient.

## SC reservation and authority

Differences and intervals are percentage points. Within-SC effects use HC2 for the three
council outcomes and GP CR2 for the two citizen outcomes, matching the author's subgroup
conventions. Interactions compare the SC effect with the non-SC effect directly. These
exploratory tests are not multiplicity-adjusted and do not identify causal mediation.

{quota_header}
|---|---:|---:|---:|---:|
{chr(10).join(quota_table)}

Council counts and both quota groups' raw means are in
[sc-authority.csv](../results/critical/sc-authority.csv). Some authority gains occur
without Maratha accession; class-based selection is still possible. The comparisons
do not show a statistically resolved amplification of authority effects under SC quotas.

## Experiment reconciliation

Raw N={flow['raw']}; blank assignment exclusions={flow['blank_assignment']};
assigned N={flow['assigned']}; all-covariate-complete N={flow['covariates_complete']}.
The paper's headline N matches authority responses, not all assigned respondents.
The original cleaning removes blank assignments and leaves missing outcomes missing.

| Outcome / assignment | Unadjusted / adjusted N | Unadjusted difference, pp | Adjusted difference [95% CI], pp |
|---|---:|---:|---:|
{chr(10).join(experiment_table)}

See [missingness by all four assigned conditions](../results/critical/experiment-missingness.csv)
and [complete estimates](../results/critical/experiment-estimates.csv).
Each outcome is a hypothetical prediction; pliability means predicted compliance with
a request to resign, and backlash means predicted threats/bullying/violence conditional
on becoming powerful and resisting. These are not realized events.

## Experimental balance: sparse-cell diagnosis

Table F.3's joint HC2 F tests are sensitive to small categories. All four Christian and
three Jain respondents in the covariate-complete sample received Kamble assignments.
The following diagnostic retains all four condition regressions. The exclusion column
localizes the extreme Wald statistic; it is not the substantive estimation sample.

| Condition | Original HC2 F / p | Ordinary F p | Excluding seven sparse-category respondents: HC2 F / p |
|---|---:|---:|---:|
{chr(10).join(balance_table)}

See [all model statistics](../results/critical/experiment-balance.csv) and
[religion cells](../results/critical/experiment-religion-cells.csv).
The [respondent-gender contingency table](../results/critical/experiment-gender-cells.csv)
has Pearson chi-square {float(gender_balance['statistic']):.3f}, df={gender_balance['df']},
p={float(gender_balance['p']):.5f}, N={gender_balance['n']}. This realized imbalance is
retained, not erased by the sparse-cell explanation. It can occur under randomization;
the release cannot verify assignment logs. Covariate adjustment was prespecified and
includes respondent gender. No main experimental estimate is replaced by this diagnostic.
"""
    (ROOT / "docs/diagnostics.md").write_text(diagnostics)


if __name__ == "__main__":
    main()
