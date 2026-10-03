PYTHON ?= python3
RSCRIPT ?= Rscript
export R_LIBS_USER = $(CURDIR)/work/authors-library

.PHONY: all verify authors audit inference critical recent note test lint format deps

all: verify authors audit inference critical recent note lint test

verify:
	$(PYTHON) analysis/preserve.py
	cd sources/institutions && shasum -a 256 -c SHA256SUMS
	cd sources/preregistration && shasum -a 256 -c SHA256SUMS

authors: verify
	$(RSCRIPT) analysis/run_authors.R > results/authors/latest-run.log 2>&1

audit: verify
	$(RSCRIPT) analysis/audit.R

inference: verify
	$(RSCRIPT) analysis/inference.R > results/inference/latest-run.log 2>&1

critical: verify
	$(RSCRIPT) analysis/critical_diagnostics.R > results/critical/latest-run.log 2>&1
	$(PYTHON) analysis/write_assessment.py

recent: verify
	$(RSCRIPT) analysis/recent_cohorts.R > results/recent/latest-run.log 2>&1
	$(PYTHON) analysis/write_recent.py

note:
	$(PYTHON) analysis/write_note.py

test: verify
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(PYTHON) -m black --check analysis/*.py tests
	$(PYTHON) -m isort --profile black --check-only analysis/*.py tests
	$(PYTHON) -m flake8 analysis/*.py tests
	$(RSCRIPT) -e 'x <- unlist(lapply(list.files("analysis", "[.]R$$", full.names=TRUE), lintr::lint), recursive=FALSE); print(x); if(length(x)) quit(status=1)'

format:
	$(PYTHON) -m black analysis/*.py tests
	$(PYTHON) -m isort --profile black analysis/*.py tests
	$(RSCRIPT) -e 'styler::cache_deactivate(); styler::style_dir("analysis")'

deps:
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(RSCRIPT) analysis/install_dependencies.R
