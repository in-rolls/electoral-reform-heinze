# Electoral institutions and the 2020 boundary

Official sources confirm different selection institutions, but they do not identify which electoral stage each survey respondent meant by “unopposed.” They also distinguish the cabinet's announced reversal from enacted law. The paper's January 2020 implementation statement requires clarification; this check does not establish that any released treatment value is erroneous.

Sources were checked on 2 October 2026. This is a historical source audit, not advice about present-day election law.

## What the official texts establish

| Source and location | Historical rule or event |
|---|---|
| State Election Commission's pre-reform compilation, section 30(1)–(2), printed p.29/PDF p.36; section 33, printed p.32/PDF p.39 | The president is chosen by and from elected council members, in the first meeting after the general election. The Collector arranges the meeting and appoints a presiding officer who cannot vote. See the [official compilation](https://mahasec.maharashtra.gov.in/Upload/PDF/6%20THE%20MAHARASHTRA%20VILLAGE%20PANCHAYATS%20ACT%20AND%20RULES.pdf). |
| Maharashtra Act LIV of 2018, titled the Maharashtra Village Panchayats (Amendment) Act, 2017; section 1(2), English p.2/PDF p.10; section 11 inserting 30A-1A, English p.4/PDF p.12 | The Act is deemed operative from **19 July 2017**. Section 30A-1A(1)–(2) provides for election by village registered voters alongside council general elections. Subsection (3) permits member selection after failure to elect a president at an initial and fresh election. Thus even this regime contains a specified exception to village-wide selection. See the [official 2018 Gazette](https://maharashtra.gov.in/Upload/PDF/13%2008%202018%20Thet%20sarpanch%20adhiniyam.pdf). |
| Government of Maharashtra, Directorate General of Information and Public Relations, *Maharashtra Ahead*, February 2020, p.40, “Selection of Sarpanch” | The government bulletin reports cabinet approval for member selection and says an ordinance **will** be issued. This records a policy decision and an intended next legislative step, not an already promulgated ordinance. See the [official February bulletin](https://dgipr.maharashtra.gov.in/sites/default/files/2020-07/MAhead-Feb2020.pdf#page=40). |
| Maharashtra Act II of 2020, Gazette dated **5 March 2020**; section 5 inserting 30A-1B, English p.2/PDF p.7; section 12, English p.4/PDF p.9 | The enacted reversal restores selection under sections 30/33. Section 12 preserves the direct-election procedure where an election order or election process began before commencement. This is not a rule depending exclusively on the eventual polling month. See the [official 2020 Gazette](https://maharashtra.gov.in/Upload/PDF/Notification%20for%20Sarpanch.pdf). |
| Same 2020 Act, section 8 amending section 43(1), English p.3/PDF p.8 | A vacancy in a directly elected president's office is to be filled from among council members within thirty days. This changes the successor-selection rule relevant during follow-up. It does not establish whether any particular survey president entered through that route. See [section 8](https://maharashtra.gov.in/Upload/PDF/Notification%20for%20Sarpanch.pdf#page=8). |
| Bombay High Court's official ordinance archive; Maharashtra Ordinance X of 2020, dated **25 June 2020**, section 2 | The similarly titled 2020 village-panchayat ordinance found in the [official index](https://bombayhighcourt.gov.in/bhc/libweb/legislation/ordins/ordinstaindex.htm) concerns appointment of administrators when elections cannot occur, including epidemic disruption. It is not a January reversal ordinance. See the [ordinance itself](https://bombayhighcourt.gov.in/bhc/libweb/legislation/ordins/2020/2020.10.pdf). |

The focused search found no official January 2020 ordinance establishing the rural reversal. Absence from this search is not proof that no relevant implementation instruction exists. The February bulletin and March Gazette nevertheless make it unsafe to equate cabinet approval with statutory commencement. The exact operative cutoff also needs the applicable commencement law and election-programme orders; it should not be silently replaced with either 1 January or a month-wide March rule.

## Reconciliation with the deposited dates

Appendix C.8, p.32 says indirect elections were passed and implemented in January 2020. President Q1/Q2 instead ask when the respondent was elected **this time as sarpanch**. Those dates need not be the council's general-election dates, the dates its election process began, or its term's starting date. [Paper appendix](../sources/appendix.pdf); [deposited instrument](https://dataverse.harvard.edu/api/access/datafile/11665676?format=original).

Direct inspection of `original/data/analysis/elite_survey.csv` identifies these boundary records:

| Anonymous council ID | President election date | `direct` | `resignation` (shared tenure) |
|---|---|---:|---:|
| 3806 | January 2020 | 1 | 1 |
| 2606 | February 2020 | 0 | 1 |
| 3955 | February 2020 | 0 | 0 |

The two February indirect presidents motivate a date-provenance check, not automatic recoding. Possible explanations include selection during an older council term, an exceptional selection route, different interpretation of the question, or inaccurate dates/coding. None is established. The response about shared tenure in council 2606 does not itself prove an earlier replacement occurred because that item also includes future plans.

The main audit's [leave-one-month-out results](../results/inference/leave_one_month_out.csv) show that excluding February 2020 changes the speaking-time gap from .051953 to .052451, the influential-actor gap from .150681 to .152429, president shared tenure from −.207200 to −.205746, and citizen shared tenure from −.179708 to −.179849. This removes two councils and up to eleven observed citizen responses, depending on the outcome. These are exclusion diagnostics, not corrected estimates; the two boundary records do not explain the large pooled gaps.

The succession amendment creates an additional conceptual distinction: a council initially elected under the direct regime can subsequently have a president selected by members. The survey asks about the incumbent's mandate, while the administrative codebook describes the regime during the tenure under study. These definitions must be reconciled before interpreting `direct` as a single, immutable council-term assignment. The release lacks successor histories and administrative dates needed to assess affected observations. This check produces **no corrected coefficient** and does not attribute any headline difference to this ambiguity.

## What “unopposed” can and cannot mean here

The law establishes a restricted member electorate for ordinary indirect presidential selection and a village electorate for ordinary direct selection. In its historical orders index, the SEC also describes declaration of an unopposed winner when one candidate remains after withdrawal, illustrating that nomination, scrutiny and withdrawal stages matter. That index entry is not a respondent-level coding key. See the [SEC orders index, entry 38, order dated 23 December 2004](https://mahasec.maharashtra.gov.in/Site/ViewPDFList?doctype=Y9ZBj6h4CCAdXxcIriFzHfeQ%2FBNzkjNfbbWDu6DDheVNLQXtZ85pmWQMrLm5ZNBZJCvstSafRvFj0Y05_3t62iQYma1aQollDfqtOOW%2F64I%3D&page=4&sort=EnumerationValue&sortdir=DESC).

President Q14 simply asks whether the respondent contested unopposed or whether others stood in competition. It does not distinguish ward-member election from internal presidential selection, count eligible or nominated candidates, or distinguish absence of nominations from withdrawals. The released 40.9% indirect versus 12.8% direct comparison therefore remains a comparison of that self-report. Legal differences strengthen the case for checking the measurement stage; they do not license assigning an unrecorded stage to each answer. The minimum resolving evidence is the original field instructions plus stage-specific nomination, withdrawal and selection records, linked through anonymous council IDs.

## Verification and preservation

The sections above were read in the official English Gazette texts and checked against the government bulletin and ordinance index. The three boundary records were independently recovered using Python's CSV reader. Downloaded primary sources in `sources/institutions/` are separate from the original Dataverse archive and its manifest. No treatment variable, author dataset, estimate, or original replication file was changed.
