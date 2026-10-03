# Literal dictionary for the headline outcomes

The deposited analytical variables reproduce response summaries, but the package does not contain the original observational survey responses or their cleaning program. `original/code/clean.R` cleans only the separate vignette experiment. Coding below therefore distinguishes the documented rule from an independently verified raw-to-analysis transformation. The latter is unavailable for the observational outcomes.

Sources: [paper](../sources/paper.pdf), [appendix](../sources/appendix.pdf), [codebook](https://dataverse.harvard.edu/api/access/datafile/11665689?format=original), [elite instruments](https://dataverse.harvard.edu/api/access/datafile/11665676?format=original), [citizen instrument](https://dataverse.harvard.edu/api/access/datafile/11665607?format=original). Appendix page numbers are the printed appendix pages. Questionnaire wording below preserves the deposited English wording, including awkward grammar. This deposit describes its instruments as the original wording for variables used in the analysis; it is not a complete export of all questions fielded.

## Population, observations, dates, and missing values

The survey contains 604 council rows: 370 indirect and 234 direct. Survey collection occurred in 2020–2022 (appendix B.1.1). Selection deliberately oversampled SC/OBC reservations and female bureaucrats; ST-reserved councils were excluded. Districts and talukas were selected under the constraints described in appendix B.1.1, rather than sampled as an unrestricted representative sample of Maharashtra.

The citizen file has 3,658 respondent rows over those 604 council IDs: 2,243 indirect and 1,415 direct. It targeted six knowledgeable key informants per council under gender/caste constraints (appendix B.1.3). Actual council counts range from 1 to 10; 543 councils have exactly six. Respondent-weighted means therefore differ conceptually from equal-council averages and are not population-weighted village resident opinions. The questionnaire's occupation categories include former officeholders. Appendix B.1.3 explicitly explains the purposive key-informant universe.

The administrative file contains 1,425 rows, with six variables only. `direct` is missing in 56 rows; `resigned` is missing in 57. Their joint complete-case sample is 1,366: 808 indirect and 558 direct. This is the denominator for Table D.8, not the number of all deposited rows. The records refer to ongoing terms at collection in summer 2022 (five weeks of manual digitization; appendix B.2). The codebook says prior-term records are destroyed and the author was not allowed to retain source-document images.

Missing fields are represented by `NA` in these CSVs. Published simple regressions exclude rows missing their outcome or treatment. The observational files do not explain item-specific missingness mechanisms or provide refusal/don't-know categories. Missingness percentages below use all rows in the relevant released file as the reference unless stated otherwise.

No observational interview dates, administrative collection dates, resignation event dates, district identifiers, or taluka identifiers are released. Elite and citizen files have `r_villageid`; the administrative file has no council ID or crosswalk. Geographic identity must not be inferred from numerical patterns in anonymized council IDs.

## Treatment and timing

| Variable | Literal source | Documented coding and limitation |
|---|---|---|
| `direct` | President Q3: “Regarding your current mandate: were you elected directly or indirectly to the sarpanch position?” | 1 direct, 0 indirect. Repeated in citizen file. Administrative codebook separately defines the regime during the tenure under study. |
| `sarpanch_election_year` | President Q1: “Which year were you elected THIS TIME as sarpanch?” | YYYY; released range 2015–2021. This wording is incumbent-specific; whether it always denotes the beginning of the entire council term needs clarification. |
| `sarpanch_election_month` | President Q2: “Which month were you elected THIS TIME as sarpanch?” | 1–12. No day is recorded. `main.R` inserts day 1 for Figure 2; that is a plotting convention. |
| `period` | Constructed in `appendix.R:475–493`, not a survey field | Early indirect: year ≤2017 and `direct=0`; direct: year 2017–2020 and `direct=1`; late indirect: year ≥2020 and `direct=0`. Counts 159, 234, 211. “Pre-2017” is loose shorthand: the first category includes indirect elections in 2017. Both transition regressions reuse period 2. |
| `reserved_women`, `reserved_open`, `reserved_obc`, `reserved_sc` | President Q4–Q7 ask whether the seat is reserved for women, OPEN, OBC, SC | Separate binary indicators. These are seat restrictions, not the president's personal characteristics. |

`months_at_risk = administrative_record_date - council_term_start_date` cannot be constructed from the deposit. An arbitrary summer-2022 endpoint does not repair the absent administrative start date, and elite survey dates cannot be joined to the administrative records. Likewise, elapsed time at the observational interview cannot be measured without the interview date. Survey collection spanned 2020–2022: older election cohorts may have been interviewed in earlier collection waves. Assigning all survey respondents one assumed interview date would conflate election timing with exposure.

## Authority outcomes

| Variable and source | Exact question | Documented coding; unit and denominator | Published number and raw-data check |
|---|---|---|---|
| `prop_speakingtime_sarpanch`; facilitated discussion Q2 | “For what approximate proportion of the discussion did the sarpanch speak? [Asked to the third-party coders]” | Continuous 0–1, joint assessment by the two enumerators at the end of the entire discussion (B.3.1). Council mean of estimated discussion shares, not a pooled stopwatch measure. N=603: indirect369/direct234; one missing council. | D.1/Figure4: indirect .259, direct .311, difference .052. CSV means .258645/.310598, difference .051953. |
| `most_influential_gd`; facilitated discussion Q1 | “Out of all of the participants in the group interview, who did you think was the most influential? [Asked to the third-party coders]” | 1 president, 0 otherwise; joint coding by two enumerators, one council observation. N=604: 370/234; none missing. Original options: 0 None, 1 Sarpanch, 2 Upa sarpanch, 3 Gram sevak, 4 Sarpanch relative, 5 Other person present. | D.1/Figure4: indirect .178, direct .329, difference .151. CSV 66/370=.178378 ; 77/234=.329060; difference .150681. |
| `i_decide_masik_sabha`; president Q8 | “Think of the last masik sabha that was held. How were decisions taken in that masik sabha?” | Response options 1 “I am the main decision-maker”, 0 “I am not the main decision-maker”. President self-report at council level. N=595: 361/234; nine missing. | D.1: indirect .211, difference .114. CSV .210526/.324786; difference .114260. |

The intended discussion convenes president, vice president, and gram sevak (B.1.4). However, the influential-actor response set explicitly accommodates extra participants and nobody being most influential. No attendance roster, original influential-actor category, vice-president speaking share, bureaucrat speaking share, or timing denominator is deposited. Neither the three-role distribution nor three-way parity can be verified from the president-only variables. A one-third comparison is a descriptive benchmark, not proof of equality across the three roles or a design-based null. Paper footnote 32, p.13 already highlights the approximately 31% speaking share and explicitly rejects interpreting presidents as autocrats.

The two citizen authority outcomes are documented with their paired capture indicators below.

## Shared tenure and administrative resignations

President Q15, underlying `resignation`, asks:

> Was/will your tenure shared/be shared with other members, or did/will you serve for the full tenure?

The response options are:

1. “I am serving the whole tenure”
2. “Someone else was sarpanch before me but I am serving the rest of the tenure only”
3. “Someone else was sarpanch before me and someone else will be sarpanch after me during this tenure only”
4. “I am the sarpanch now but someone will be sapranch after me in this tenure only”

The codebook defines `resignation=1` as sharing tenure, zero as not sharing. Appendix B.3.2 gives the equivalent multiple-presidents versus full-term rule. Combining options 2–4 is implied by that documentation, but cannot be independently checked because the four-category field and cleaning code are absent. Crucially, the binary combines retrospective replacement, prospective rotation, and both; it is not a completed-resignation event for the interviewed president.

Citizen Q3, underlying `resignation_reported`, asks:

> In the current gram panchayat period, has there been more than one sarpanch or will there be more than one sarpanch (meaning has/will some sarpanch gave/give their resignation so another could be sarpanch, possibly to rotate the position)?

Yes = 1, no = 0. This is a knowledgeable informant's report of actual **or anticipated** multiple presidents. It is independently reported by another respondent but measures the same council tenure and does not separate plans from events.

| Variable | Denominator and missingness | Published Table D.8 | Direct CSV reconstruction |
|---|---|---|---|
| `resignation`, elite | N = 601: indirect 369/direct 232; 3 missing | indirect .233; difference −.207 |86/369=.233062 ; 6/232=.025862; difference −.207200 |
| `resignation_reported`, citizen | N = 3578: 2179/1399; 80 missing | indirect .210; difference −.180 | .209729/.030021; difference −.179708 |
| `resigned`, administrative | N = 1366: 808/558; 59 rows excluded for missing outcome or regime | indirect .193; difference −.138 |156/808=.193069 ; 31/558=.055556; difference −.137514 |

The administrative definition is at least one filed presidential resignation during the ongoing council tenure. It is a cumulative binary council event, not a resignation count, instantaneous hazard, or completed-five-year risk. Collection was in summer 2022; exact record and event dates are absent. The full source documents are also absent.

An exposure concern must not assume that direct councils had less time to resign. **If** the paper's assignment timeline maps to the ongoing administrative terms, councils elected directly during July 2017–January 2020 would generally have older terms at the summer-2022 collection than indirect councils elected in 2020–2021. That would suggest more exposure for the direct cohort, potentially the opposite of an explanation attributing its lower cumulative resignation frequency to less exposure. This is a conditional implication of the timeline, not an observed comparison of administrative term ages: the administrative file's actual election-date distribution is absent and cannot be inferred from the separate survey sample. A verified common-risk adjustment remains unavailable.

Table D.10's early/direct/late means are .418/.026/.095 for president shared tenure and .390/.030/.069 for citizen reports; these are different cross-sectional councils, not within-council changes. Appendix D.2.6 followed up the 92 presidents with positive survey responses; 87 answered, and 71 attributed decisions to influential villagers. The selected follow-up supports the presence of elite-directed rotations among positive reports, but is not a validation sample for all zero reports or evidence separating time at risk from institutional effects.

## Unopposed election

President Q14 asks: “Did you contest unopposed, or were there others who stood in the competition?” Options are 1 “Unopposed” and 0 “Others were there”. `sarpanch_uncontested` follows this binary rule. N = 603: 369 indirect/234 direct; one missing. Table D.8 reports .409 indirect and−.281 difference; CSV151/369=.409214 and30/234=.128205, difference −.281009.

The deposited question does **not** specify whether an indirectly elected president is describing her ward-member election or the subsequent internal presidential selection. Paper Table1,p.6 distinguishes both institutional stages; qualitative discussion on p.10 and appendix D.2.7 discusses uncontested ward candidacies and form withdrawals as well. There are no candidate rosters, nomination/withdrawal records, stage-specific questions, vote counts, or procedural coding rules in the release. The regime comparison of this report is reproducible; equal measurement of a specific electoral-stage event is not established. Paper p.15 explicitly acknowledges that its data cannot test whether unopposed elections result from elite manipulation.

## Rich-landowner influence

President Q16 asks: “Is there a person in this village, like a village patil, who owns the majority of the land, is quite rich, and is important around here?” Q17 asks: “If yes to question above, do they influence gram panchayat decisions and work?” Each has yes 1/no 0 responses.

`rich_landowner_influences_gp` is documented as1 when the president reports such influence and 0 otherwise. Its N = 588 comprises 359 indirect/229 direct; 16 councils are missing. Table D.8 reports .131 indirect and−.083 difference; CSV47/359=.130919 and11/229=.048035, difference −.082884.

The composite appears to combine existence and influence, rather than conditioning its denominator solely on councils where a rich landowner exists. The individual Q16/Q17 values and skip/missing-value transformations are unavailable, so this cannot be independently reconstructed. The wording does not explicitly require the person to be outside elected office, whereas the paper p.13 describes a landowner “not elected to the council.” The broader claim therefore relies on interviewer implementation or information absent from the deposited questions. Treatment-dependent reporter composition and the distinction between external and total elite influence remain measurement concerns; the observed decline does not by itself identify a change in total elite control.

## Caste land share and the other formal-capture indicators

Bureaucrat Q10 asks: “On average approximately what proportion of land does the sarpanch’s jati own in this GP’s villages?” `avg_prop_land_held_sarpanch_caste` is the 0–1 approximate average reported by the gram sevak. The questionnaire does not elicit plot-level ownership, specify an area-weighting rule across constituent villages, or supply records allowing that average to be checked. It is a caste-group land-share proxy, not the president's personal landholding.

Table D.7 reports N = 382, indirect .289 and difference +.154. The CSV has215 indirect observations with mean .288702 and167 direct with mean .442884 (difference .154183). Missing are 155/370 indirect and 67/234 direct councils, totaling 222/604=36.75%. By the authors' period categories only 6/159 early-indirect councils,167/234 direct councils, and209/211 late-indirect councils have observations. The near absence of the early group is critical to interpreting the pooled comparison. District/taluka missingness cannot be assessed with released fields; missingness by treatment, quota, Maratha status and election year/month can be.

| Released indicator | Literal question/response | Measurement qualification |
|---|---|---|
| `sarpanch_maratha` | President Q9: “Are you Maratha?” yes 1/no 0 | This identifies one caste identity, not general elite status. N = 603. |
| `sarpanch_male` | Q10: “What is the gender of the respondent?” Male 1/Female 2/Third gender 3 | Codebook says male 1/female 0; raw handling of third gender is not shown. N = 604. |
| `sarpanch_land_own_name` | Q11: “Do you, as an individual, currently own or plan to inherit any land?” yes 1/no 0 | Paper/codebook describe ownership in own name, but deposited wording includes intended inheritance. N = 596; Table D.7 difference +.155; CSV .334247/.489177. Actual ownership alone cannot be recovered. |
| `three_four_wheeler` | Q12: “Does your household own any of the following vehicles (check all that apply):” Car, Three wheeler, Two wheeler, Bicycle, Other | Household asset, not necessarily individually owned by president. Published binary car/three-wheeler versus otherwise; raw checkboxes absent. N = 604. |
| `pacca_house` | Q13: “Which of the following best describes the house in which you live?” Full pacca, mixed pacca/kaccha, kaccha, hut | Dwelling construction material; deposited wording does not ask legal ownership, despite “owns” labels. N = 604. |

## Citizen questions and categorical dependence

Citizen Q1 asks:

> Suppose next month there will be a meeting with the Block Development Officer in which decisions about how to resolve your village’s most urgent development problems will be made. You get to nominate one person to go and represent your village’s interests in the meeting. This can be anyone. Of course, this is by law something that falls within the duties of the sarpanch. Who would you like to nominate? We’re collecting nominations from villagers.

The nine response options are: 1 Current sarpanch; 2 Former sarpanch; 3 Upa sarpanch; 4 Gram sevak; 5 Someone else from the gram panchayat; 6 Someone from the sarpanch’s household; 7 Someone else who used to be a member of the gram panchayat; 8 Someone else from the village NOT in the GP and NOT in the HH; 9 Other.

`sarpanch_nominate_BDO` is 1 for current president, 0 otherwise. `other_nominate_BDO` is 1 for former president, former member or other non-GP/non-household villager (documented rule implies options 2, 7, 8). Both have N = 3603 and 55 missing values. Published D.1: current-president indirect .583, difference +.082. D.8: outside-category indirect .168, difference −.052. This is an elicited nomination under an explicitly presidential-duty prompt, not observation of a realized meeting.

Citizen Q2 asks:

> Think about this village. At inaugural events or programs who tends to be the head? For example, this might mean, who delivers the speech?

Its eight options are: 1 Current sarpanch; 2 Former sarpanch; 3 Gram sevak; 4 Upa sarpanch; 5 Another gp member; 6 Spouse of sarpanch; 7 Family member; 8 Other.

`sarpanch_inauguralevents` is 1 for current president. `formersarpanch_otherperson_inauguralevents` is 1 for former president or another villager, excluding current GP and family members (B.3.2). The documented categories imply 2/8, but handling of “Other” needs original responses or cleaning code for verification. Both have N = 3536 and 122 missing values. Published D.1: current-president indirect .617, difference +.132. D.8: outside-category indirect .205, difference −.057.

Paired indicators are mutually exclusive in every observed row and have identical missingness. Three **coarse** exhaustive categories can therefore be reconstructed: current president, published outside group, and all remaining observed answers. The complete nine/eight-category distributions cannot.

| Question and regime | Current president | Published outside category | Remaining categories | Observed denominator |
|---|---:|---:|---:|---:|
| BDO, indirect |1287 (58.288%)|370 (16.757%)|551 (24.955%)|2208|
| BDO, direct |927 (66.452%)|161 (11.541%)|307 (22.007%)|1395|
| Events, indirect |1340 (61.666%)|445 (20.479%)|388 (17.855%)|2173|
| Events, direct |1020 (74.835%)|201 (14.747%)|142 (10.418%)|1363|

Thus the two capture indicators do not constitute two new independent survey questions in addition to the authority indicators. They also are not simply `1 - president`: other council and family categories account for the remaining mass.
