# Electoral Reform in Rural India

Replication and analysis of *“Democratic Deepening or Elite Persistence? How Local Elites Adapt to Electoral Reform in Rural India”* by Alyssa R. Heinze (APSR).

The released code reproduces all 28 deposited tables and the 161 checked main-figure labels. This repository documents the outcome definitions, comparison-group levels, election-cohort patterns and uncertainty behind those results.

The survey covers 604 Maharashtra gram panchayats: 234 with directly elected presidents and 370 with indirectly elected presidents. Citizen respondents are purposively selected knowledgeable informants. Administrative resignation records and a randomized vignette provide separate measures.

## Discussion participation

<!-- generated:authority -->

| Outcome | Indirect | Direct | Observed councils, indirect / direct |
|---|---:|---:|---:|
| President judged most influential | 17.8% | 32.9% | 370 / 234 |
| President speaking share | 25.9% | 31.1% | 369 / 234 |

<!-- /generated:authority -->

Directly elected presidents have higher observed speaking shares and are more often judged most influential. The indirect-president baseline needs an institutional explanation: the formal council head accounts for about a quarter of speaking time and is judged most influential in fewer than one in five discussions. Bureaucratic expertise, proxy officeholding and authority exercised with little speech are possible explanations; the released president-only measures cannot distinguish them. The intended discussion includes the president, vice president and bureaucrat, but the instrument permits additional participants and a “none” response. Other actors' shares and attendance are unavailable, so one-third is only a descriptive reference. [Outcome definitions](docs/data-dictionary.md#authority-outcomes).

## Shared tenure and election cohorts

<!-- generated:cohorts -->

| Outcome | Early indirect | Direct | Later indirect |
|---|---:|---:|---:|
| President reports shared tenure | 41.8% (66/158) | 2.6% (6/232) | 9.5% (20/211) |
| Citizen reports shared tenure | 39.0% (372/953) | 3.0% (42/1399) | 6.9% (85/1226) |
| President reports unopposed selection | 43.4% (69/159) | 12.8% (30/234) | 39.0% (82/210) |

<!-- /generated:cohorts -->

Shared-tenure reports differ substantially between the two indirect-election cohorts, while unopposed-selection reports are similar. The tenure question includes both previous and planned sharing; it is not a completed-resignation rate. Early indirect includes five early-2017 councils; later indirect refers to elections in 2020 or 2021. Both transition comparisons use the same direct-election cohort.

Removing early indirect councils reduces the shared-tenure contrasts; also removing older direct councils reduces the most-influential contrast. Speaking shares and citizen-reported event leadership remain higher, and unopposed-selection reports remain lower, among direct presidents in the recent comparisons. The 2019-onward sample has only 27 direct councils versus 211 indirect councils. [All 17 outcomes, counts and confidence intervals](docs/cohorts.md).

Direct-minus-indirect differences, in percentage points:

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

Dropping early indirect councils retains all direct councils. The 2018 and 2019 cutoffs instead restrict both arms, leaving 86 and 27 direct councils against 211 later indirect councils. These are different comparisons. The within-indirect change from 41.8% to 9.5% requires an explanation involving calendar time, term age, rotation norms, replacement or reporting before the pooled difference is attributed to election method. Missing interview and term-start dates prevent separating these explanations.

## Selection institutions and reporting

An unopposed selection among council members and an unopposed village-wide election arise from different candidate pools and nomination processes. The deposited question does not establish which selection stage indirect presidents describe, limiting comparability as a measure of capture.

Rich-landowner influence falls from about 13.1% to 4.8% in presidents' reports. Electoral reform can change both who holds the presidency and the reporter's incentives. Elites moving into office and changes in acknowledged dependence are possible explanations; the item does not independently measure total elite influence. Some citizen authority and outside-influence indicators are also categories of the same two questions, rather than independent measurements. [Definitions and code](docs/data-dictionary.md).

## Officeholder composition and elite control

Officeholder caste, gender and assets describe composition. Selected village histories document elite adaptation, and the vignette measures expectations about hypothetical presidents. Neither advantaged officeholding nor fewer reports of outside influence directly establishes whose interests determine decisions or whether accountability improves. Persistent capture and more accountable elite leadership are both compatible with that pattern. Representative evidence on decisions and beneficiaries is needed to distinguish them. [Interpretation and supporting evidence](docs/interpretation.md).

## Coverage, exposure and uncertainty

The caste-land measure is a bureaucrat's approximate assessment. Its coverage varies by cohort:

<!-- generated:land -->

| Early indirect | Direct | Later indirect |
|---:|---:|---:|
| 6/159 councils observed | 167/234 councils observed | 209/211 councils observed |

<!-- /generated:land -->

Only 382 of 604 councils have this measure, and just six are early indirect councils. The pooled land comparison therefore mainly represents the direct and later indirect cohorts.

Administrative filed resignations are a separate outcome: 19.3% of indirect versus 5.6% of direct councils have at least one recorded event. A cumulative event indicator depends on time at risk. Election, event and record dates are unavailable, so comparable-exposure risks cannot be estimated; the direction of exposure bias is not established.

Election-month clustering changes uncertainty for some outcomes. District/taluka identifiers are absent, preventing geographic clustering and fixed-effects checks. Original observational responses, construction code and interview dates are also unavailable. Clustering cannot resolve outcome definitions or cohort comparability. [Methods and data limits](docs/methods.md).

## Replication materials

| Directory | Contents |
|---|---|
| [sources/](sources/) | Original archive, papers, institutional records and checksums |
| [scripts/](scripts/) | Data verification, estimation and report generation |
| [results/](results/) | Tables, figures, estimates and execution logs |
| [tests/](tests/) | Independent arithmetic and sample checks |
| [docs/](docs/) | Variable definitions, methods and detailed results |

The [numerical summary](docs/audit.md), [measurement table](docs/claims.md) and [reproduction record](docs/reproduction.md) link findings to the underlying data and code. The [cohort analysis](docs/cohorts.md) reports alternative samples and inference methods without selecting outcomes by significance. These are exploratory analyses; election-cohort restrictions do not supply within-council pre/post outcomes or equalize term age.

## Reproduce locally

```sh
python3 -m venv .venv
. .venv/bin/activate
make deps
make all
```

The verified environment uses R 4.6.0 and Python 3.14.7; the original code specified R 4.4.3. Package versions and execution differences are recorded in the [reproduction notes](docs/reproduction.md). Dependency installation requires network access; the data are bundled.

`make all` verifies sources, runs the original code and additional analyses, regenerates reports, and runs tests and linting. `make test` checks retained results independently against source data. `make ci-docker` runs the Python verification tier in the standard Python 3.14 image. Hosted CI verifies that tier and R linting; complete R estimation is run locally.

Paper: [10.1017/S0003055425101068](https://doi.org/10.1017/S0003055425101068). Replication: [10.7910/DVN/QGH7P4](https://doi.org/10.7910/DVN/QGH7P4), version 1.0. The unchanged 113-file archive, checksums, attribution and reuse terms are documented in [sources/README.md](sources/README.md).
