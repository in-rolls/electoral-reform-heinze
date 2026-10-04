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

Directly elected presidents have higher observed speaking shares and are more often judged most influential. Understanding the indirect-president levels also requires information about the other participants. The intended discussion includes the president, vice president and bureaucrat, but the instrument permits additional participants and a “none” response. Other actors' shares and attendance are unavailable, so one-third is only a descriptive reference. [Outcome definitions](docs/data-dictionary.md#authority-outcomes).

## Shared tenure and election cohorts

<!-- generated:cohorts -->

| Outcome | Early indirect | Direct | Later indirect |
|---|---:|---:|---:|
| President reports shared tenure | 41.8% (66/158) | 2.6% (6/232) | 9.5% (20/211) |
| Citizen reports shared tenure | 39.0% (372/953) | 3.0% (42/1399) | 6.9% (85/1226) |
| President reports unopposed selection | 43.4% (69/159) | 12.8% (30/234) | 39.0% (82/210) |

<!-- /generated:cohorts -->

Shared-tenure reports differ substantially between the two indirect-election cohorts, while unopposed-selection reports are similar. The tenure question includes both previous and planned sharing; it is not a completed-resignation rate. Early indirect includes five early-2017 councils; later indirect refers to elections in 2020 or 2021. Both transition comparisons use the same direct-election cohort.

Restricting election cohorts reduces the shared-tenure and most-influential contrasts. Speaking shares and citizen-reported event leadership remain higher, and unopposed-selection reports remain lower, among direct presidents in the recent comparisons. The 2019-onward sample has only 27 direct councils versus 211 indirect councils. [All 17 outcomes, counts and confidence intervals](docs/cohorts.md).

## Measurement and coverage

Unopposed reports can refer to different selection stages under the two electoral systems. Landowner-influence reports come from presidents, and some citizen authority and influence indicators are categories of the same questions. These distinctions matter when comparing the measures across regimes.

Officeholder caste, gender and assets describe composition. Selected village histories document elite adaptation, and the vignette measures expectations about hypothetical presidents. Representative evidence on decision-making and beneficiaries would help connect those measures to changes in elite control. [Interpretation and supporting evidence](docs/interpretation.md).

The caste-land measure is a bureaucrat's approximate assessment. Its coverage varies by cohort:

<!-- generated:land -->

| Early indirect | Direct | Later indirect |
|---:|---:|---:|
| 6/159 councils observed | 167/234 councils observed | 209/211 councils observed |

<!-- /generated:land -->

Original observational responses, construction code, interview dates, administrative event dates and geographic identifiers are not included in the release. Their availability would permit further measurement, exposure and dependence analyses. [Methods and data limits](docs/methods.md).

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
