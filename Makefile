PYTHON ?= python3
RSCRIPT ?= Rscript
export R_LIBS_USER = $(CURDIR)/work/authors-library

.NOTPARALLEL:

.PHONY: all verify authors audit inference critical recent note readme test lint lint-python lint-r ci-python ci-docker format deps

all: verify authors audit inference critical recent note readme lint test

verify:
	$(PYTHON) scripts/preserve.py
	cd sources/institutions && shasum -a 256 -c SHA256SUMS
	cd sources/preregistration && shasum -a 256 -c SHA256SUMS

authors: verify
	$(RSCRIPT) scripts/run_authors.R > results/authors/latest-run.log 2>&1

audit: verify
	$(RSCRIPT) scripts/audit.R

inference: verify
	$(RSCRIPT) scripts/inference.R > results/inference/latest-run.log 2>&1

critical: verify
	$(RSCRIPT) scripts/critical_diagnostics.R > results/critical/latest-run.log 2>&1
	$(PYTHON) scripts/write_assessment.py

recent: verify
	$(RSCRIPT) scripts/recent_cohorts.R > results/recent/latest-run.log 2>&1
	$(PYTHON) scripts/write_recent.py

note:
	$(PYTHON) scripts/write_note.py

readme:
	$(PYTHON) scripts/write_readme.py

test: verify
	$(PYTHON) -m unittest discover -s tests -v

lint: lint-python lint-r

lint-python:
	$(PYTHON) -m black --check scripts/*.py tests
	$(PYTHON) -m isort --profile black --check-only scripts/*.py tests
	$(PYTHON) -m flake8 scripts/*.py tests

lint-r:
	$(RSCRIPT) -e 'x <- unlist(lapply(list.files("scripts", "[.]R$$", full.names=TRUE), lintr::lint), recursive=FALSE); print(x); if(length(x)) quit(status=1)'

ci-python: test lint-python
	$(PYTHON) scripts/write_readme.py --check

ci-docker:
	docker run --rm -v "$(CURDIR):/audit" -w /audit python:3.14 bash -c 'pip install -r requirements-dev.txt && make ci-python'

format:
	$(PYTHON) -m black scripts/*.py tests
	$(PYTHON) -m isort --profile black scripts/*.py tests
	$(RSCRIPT) -e 'styler::cache_deactivate(); styler::style_dir("scripts")'

deps:
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(RSCRIPT) scripts/install_dependencies.R
