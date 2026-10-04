# Presidential, in Principle

An independent replication and audit of Alyssa R. Heinze's *“Democratic Deepening or Elite Persistence? How Local Elites Adapt to Electoral Reform in Rural India”* (APSR).

The published summaries reproduce. The larger questions concern what the comparison-group levels mean, why reported tenure sharing changes so sharply within the indirect-election regime, and whether the measured differences establish changes in elite capture. Several associations survive the audit. Reproduction establishes the calculations; the measurement and causal interpretations require separate evidence.

The survey covers 604 gram panchayats in Maharashtra, with 234 directly and 370 indirectly elected presidents. Citizen respondents are purposively selected knowledgeable informants. The administrative resignation census and randomized vignette are separate datasets and answer different questions.

## Five principal findings

### The authority baseline needs an institutional explanation

<!-- generated:authority -->

| Outcome | Indirect | Direct | Observed councils, indirect / direct |
|---|---:|---:|---:|
| President judged most influential | 17.8% | 32.9% | 370 / 234 |
| President speaking share | 25.9% | 31.1% | 369 / 234 |

<!-- /generated:authority -->

The indirect president is rarely singled out as the most influential participant. Who commands these discussions instead, and what does that imply about the presidency? Bureaucratic expertise, proxy officeholding, and authority exercised with little speech are possible accounts; the released president-only variables cannot distinguish them.

The intended discussion includes the president, vice president and bureaucrat, but the instrument also accommodates relatives, other participants and nobody being most influential. Attendance and other actors' shares are unavailable. One-third is a descriptive reference, not an established institutional norm or a statistical null. The direct-president levels are compatible with a relative authority gain; the paper itself notes that these presidents are not autocrats. **Status: unresolved baseline interpretation and incomplete measurement, not a demonstrated numerical error.** [Questions, coding and denominators](docs/data-dictionary.md#authority-outcomes).

### Shared tenure changes dramatically within the indirect regime

<!-- generated:cohorts -->

| Outcome | Early indirect | Direct | Later indirect |
|---|---:|---:|---:|
| President reports shared tenure | 41.8% (66/158) | 2.6% (6/232) | 9.5% (20/211) |
| Citizen reports shared tenure | 39.0% (372/953) | 3.0% (42/1399) | 6.9% (85/1226) |
| President reports unopposed selection | 43.4% (69/159) | 12.8% (30/234) | 39.0% (82/210) |

<!-- /generated:cohorts -->

The tenure-sharing collapse occurs between different councils under the same nominal election regime. Unopposed selection stays high in both indirect cohorts. The questionnaire combines previous and planned tenure sharing, so the early rate cannot be read as the proportion of presidents who already resigned. Calendar change, exposure, replacement, reporting and rotation norms remain competing explanations.

“Early indirect” includes five early-2017 councils; later indirect councils were elected in 2020 or 2021. Both transition comparisons reuse the same direct-election cohort. **Status: verified cohort sensitivity and a measurement mismatch between shared tenure and completed resignation.** [Counts, recent restrictions and uncertainty](docs/cohorts.md).

### The informal-capture measures are not institutionally interchangeable

Unopposed internal selection and an unopposed village-wide election need not measure the same event. The deposited question does not resolve which electoral stage an indirect president describes. The rich-landowner measure comes from presidents whose identity and incentives may themselves change with election rules; it does not independently measure total elite power. Citizen authority and outside-influence indicators also reuse categories from two underlying questions.

These are reproducible differences in specific reports. A common interpretation as reduced informal capture needs comparable selection stages, reporting and constructs. **Status: verified wording and question reuse; reporting bias and the extent of capture remain unresolved.** [Questions and coding](docs/data-dictionary.md).

### Officeholder privilege does not establish persistence of elite control

Caste, gender and assets describe who occupies office. They do not directly measure whose interests determine decisions or whether accountability improves. Selected village histories document elite adaptation, and the randomized vignette identifies effects of described identity on respondents' expectations. Their contribution is real but narrower than a representative measure of continuing elite control or an identified mediation effect of electoral reform.

**Status: a gap between measured composition, case evidence and the sample-wide mechanism claim.** [Claim-by-claim assessment, including the author's defenses](docs/claims.md).

### Missing records limit substantive checks

The caste-land measure is a bureaucrat's approximate assessment, with observation concentrated in particular cohorts:

<!-- generated:land -->

| Early indirect | Direct | Later indirect |
|---:|---:|---:|
| 6/159 councils observed | 167/234 councils observed | 209/211 councils observed |

<!-- /generated:land -->

The pooled comparison is consequently dominated by later indirect councils. Original observational responses and construction code, interview and administrative event dates, and geographic identifiers are also absent from the release. These omissions limit construction, exposure and dependence checks. **Status: verified missingness and audit limits; the direction of resulting bias is not established.** [Scope and data limits](docs/methods.md#scope-and-data-limits).

## What survives the audit

The unedited author workflow reproduces all 28 deposited tables, including 2,925 printed numerical cells, and 161 checked main-figure labels. All 12 figures regenerate; the scope of the numerical and graphical comparisons is documented in the [execution record](docs/reproduction.md).

Lower unopposed-selection reports, greater president speaking time and higher citizen-reported event leadership persist in the recent-cohort comparisons. Their uncertainty varies by method, and their causal or capture interpretation still requires the assumptions above. Some composition differences also persist. Qualitative evidence establishes adaptation in selected cases, and the vignette's main quantitative analyses reconcile with its disclosed registration timing. The [four-section audit note](docs/audit.md) separates these results from a small verified descriptive-standard-error error and other qualifications.

## How analytical choices matter

Raw direct-minus-indirect differences, in percentage points:

<!-- generated:contrasts -->

| Outcome | Original pooled | Drop early indirect | Both regimes: 2018 onward | 2019 onward |
|---|---:|---:|---:|---:|
| President judged most influential | 15.07 | 15.37 | 5.72 | 4.69 |
| President speaking share | 5.20 | 5.13 | 5.17 | 6.10 |
| President reports shared tenure | -20.72 | -6.89 | -5.95 | -2.07 |
| Citizen reports shared tenure | -17.97 | -3.93 | -4.61 | -3.21 |
| President reports unopposed selection | -28.10 | -26.23 | -21.61 | -27.94 |
| Citizen says president leads events | 13.17 | 15.56 | 15.53 | 17.16 |

<!-- /generated:contrasts -->

Dropping early indirect councils retains every direct council. The other restrictions remove older councils from both regimes. The 2018 and 2019 restrictions leave 86 and 27 direct councils respectively, compared with 211 later indirect councils. Only one direct council remains from 2020 onward and none from 2021 onward. These are election-cohort restrictions, not comparisons at equal term age or within-council changes.

The [complete recent-cohort results](docs/cohorts.md) report all 17 survey outcomes, denominators, confidence intervals, original-method inference, election-month clustering with small-sample adjustments, and wild-bootstrap inference. The later indirect arm occupies only five election-month clusters. The [inference audit](docs/methods.md) and [critical diagnostics](docs/diagnostics.md) examine additional specifications and the author's omitted-confounding sensitivity argument. These analyses are exploratory; no multiplicity-adjusted confirmatory claim is made.

Different estimators can be credible under different assumptions. A controlled cross-section needs justified adjustment and overlap; difference-in-differences needs supported group-by-time outcome comparisons and a credible parallel-trends argument. Election cohorts do not supply pre/post outcomes by themselves. Clustering addresses uncertainty, not the meaning of an outcome or the credibility of its baseline.

## What would resolve the uncertainties

| Missing evidence | Question it would answer |
|---|---|
| Attendance, full influential-actor categories and all speaking shares | Who commands the discussions, and what is the speaking-time denominator? |
| Original sharing categories, term starts, interview dates and succession histories | How much is completed turnover, anticipated rotation, term age or calendar change? |
| Administrative election, resignation and censoring dates | Do filed resignation risks differ at comparable exposure? |
| Stage-specific nominations and candidate records | Are unopposed reports comparable, and do they reflect elite coordination? |
| Original land assessments, item-administration records and anonymous geography | Why is land measurement cohort-selected, and how does geographic dependence affect inference? |
| Representative elite-network and decision-beneficiary evidence | Does advantaged officeholding preserve control over policy and benefits? |

No authors or third parties have been contacted. Unavailable evidence is recorded as an audit limit, not as evidence that the opposite claim is true.

## Reproduce locally

The completed run used R 4.6.0 and Python 3.14.7. The author specified R 4.4.3; the software-version deviation and actual package versions are recorded under `results/authors/`. Preserved author code is unedited and runs in a disposable copy.

```sh
python3 -m venv .venv
. .venv/bin/activate
make deps
make all
```

The Makefile serializes the analysis targets. `make all` verifies sources, runs the author pipeline and all audit analyses, generates the reports and README tables, and runs Python/R linting and independent arithmetic tests. The bundled data need no API key or new download. Installing dependencies requires CRAN/GitHub access and native build tools when binaries are unavailable. The bootstrap dependency is pinned to its recorded upstream commit.

`make test` independently checks retained results against source data; it does not rerun R estimation. `make recent` regenerates the recent-cohort analysis from existing baseline outputs. `make readme` updates only the marked numerical tables from analysis outputs. The main inference bootstrap uses seed 20261002; the recent-cohort follow-up uses 20261003. Both request 9,999 draws, with actual enumeration counts recorded in the outputs.

GitHub Actions verifies source hashes, independently checks the retained numerical results, checks generated README tables, and runs Python/R linting. The complete R analysis is verified locally for release. `make ci-docker` runs the Python verification tier in the standard Python 3.14 image.

## Replication materials

| Directory | Contents |
|---|---|
| [sources/](sources/) | Original archive, papers, institutional records and checksums |
| [scripts/](scripts/) | Data verification, R estimation and report generation |
| [results/](results/) | Tables, figures, full-precision estimates and execution logs |
| [tests/](tests/) | Independent arithmetic and sample-conservation checks |
| [docs/](docs/) | Audit findings, variable definitions, methods and interpretation |

## Evidence and sources

- [Four-section audit note](docs/audit.md) and [critical assessment](docs/interpretation.md)
- [Claim ledger](docs/claims.md), [variable dictionary](docs/data-dictionary.md), and [institutional rules](docs/institutions.md)
- [Raw means and denominators](results/audit/raw-means.csv), [cohort means](results/audit/cohort-means.csv), and [all recent-cohort estimates](results/recent/estimates.csv)
- [Execution record](docs/reproduction.md), [audit coverage](docs/methods.md#scope-and-data-limits)

Paper: [10.1017/S0003055425101068](https://doi.org/10.1017/S0003055425101068). Replication: [10.7910/DVN/QGH7P4](https://doi.org/10.7910/DVN/QGH7P4), version 1.0, published October 30, 2025.

`sources/dataverse-v1.0-original.zip` preserves the complete, unchanged 113-file download. Every deposited file matches its Dataverse MD5; [SHA-256 checksums](sources/SHA256SUMS) and the [manifest](sources/file-manifest.csv) preserve provenance. `make verify` extracts absent files and checks existing files without silently replacing changed sources. `original/` and disposable `work/` are ignored by Git. The deposit's nested Git metadata remains inside the preserved archive.

Source acquisition, attribution and reuse terms are recorded in [sources/README.md](sources/README.md). This is an independent audit, not an author-endorsed correction.
