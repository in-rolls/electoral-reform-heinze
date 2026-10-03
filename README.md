# Heinze electoral-reform replication and audit

Replication of Alyssa R. Heinze, **“Democratic Deepening or Elite Persistence? How Local Elites Adapt to Electoral Reform in Rural India”**, and an arithmetic-first audit of its headline claims.

- [Four-section audit note](docs/audit-note.md)
- [Literal variable dictionary](docs/variable-dictionary.md)
- [All headline means, denominators, uncertainty and cohort means](results/audit/raw-means.csv)
- [Author-code execution and numerical comparisons](docs/execution.md)
- [Inference diagnostics](docs/inference.md)
- [Measurement findings and unavailable checks](docs/measurement-review.md)
- [Official institutional rules and unresolved 2020 timing boundary](docs/institutions.md)
- [Audit coverage matrix](docs/check-matrix.md)

The unedited author workflow reproduces all 28 deposited tables (2,925 printed numerical cells) and 161 checked main-figure labels. Main concerns involve planned/shared tenure labeled resignation, cohort differences, concentrated land-measure missingness, dependence, and reused citizen questions. These are distinguished from a small verified balance-table SE error. Several requested checks require data omitted from the public release; they are explicitly marked unavailable.

## Reproduce locally

The completed run used R 4.6.0 and Python 3.14.7. R 4.4.3 was specified by the author but is not installed here. Full actual package versions and original execution errors are retained in `results/authors/`. The author code installs its deposited `pwtest` package in a repository-local R library; it remains unedited.

```sh
python3 -m venv .venv
. .venv/bin/activate
make deps
make all
```

`make all` verifies the sources, executes the full author pipeline in a disposable copy, runs the independent audit and inference diagnostics, regenerates the note, runs black/isort/flake8/lintr, and runs independent arithmetic tests. Bootstrap inference uses 9,999 draws and seed 20261002. Logs and outputs are under `results/`. Use ordinary `make all`, without `-j`, to preserve audit order.

The public data are bundled; no data download or API key is needed to rerun. Initial dependency installation needs CRAN/GitHub access and native build tools if binary R packages are unavailable. The bootstrap dependency is installed from its upstream 0.14.3 commit, matching this run. `make test` checks existing results; `make audit` and `make inference` regenerate their respective outputs. Development linting covers the new audit code; preserved author code is not restyled.

## Sources and preservation

Paper: [10.1017/S0003055425101068](https://doi.org/10.1017/S0003055425101068). Replication: [10.7910/DVN/QGH7P4](https://doi.org/10.7910/DVN/QGH7P4), **version 1.0**, published October 30, 2025.

`sources/dataverse-v1.0-original.zip` is the unmodified complete Dataverse download. All 113 deposited files match their Dataverse MD5 checksums. [SHA-256 checksums](sources/SHA256SUMS) protect the archive, metadata, paper and appendix; the [file manifest](sources/file-manifest.csv) records individual hashes, sizes and file IDs. `make verify` extracts absent files and checks existing files against both archive bytes and the manifest. It never silently replaces a changed source.

`original/` is extracted from the archive and ignored by Git; `work/` contains disposable execution copies and local dependencies. The archive preserves even the deposit's nested Git metadata. Original questionnaires, code and data remain unchanged. See [source URLs and acquisition record](sources/README.md) and the deposit's own license metadata for source reuse terms.

This repository is an independent audit, not an author-endorsed correction. No authors or third parties were contacted.
