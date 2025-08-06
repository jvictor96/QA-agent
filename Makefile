#!/usr/bin/env make

PROJECT		:= langchain_project
RM			:= rm -rf
PYTHON		:= python3
COVERAGE	:= 90

.DEFAULT_GOAL	:= test

.PHONY: all badge clean cleanall doc format help lint preen report test lint_unsafe sync

all: test report

help:
	@echo
	@echo "Default goal: ${.DEFAULT_GOAL}"
	@echo
	@echo "  all:    style and test"
	@echo "  badge:  generate project badges"
	@echo "  clean:  delete all generated files"
	@echo "  doc:    generate html reports and pdoc"
	@echo "  format: format code, sort imports and requirements"
	@echo "  lint:   check code"
	@echo "  preen:  format and lint"
	@echo "  report: doc and badge"
	@echo "  test:   preen and run unit tests"
	@echo
	@echo "To setup/update the development environment (creates .venv and installs all dependencies):"
	@echo "  make sync"
	@echo
	@echo "After running 'make venv', activate the environment with:"
	@echo "  source .venv/bin/activate          (*nix)"
	@echo "  .venv\\Scripts\\activate           (Windows)"
	@echo
	@echo "Deactivate with:"
	@echo "  deactivate"
	@echo

format:
	ruff format
	taplo format pyproject.toml

lint:
	ruff check --output-format grouped --fix
	taplo lint pyproject.toml

lint_unsafe:
	ruff check --unsafe-fixes --fix --show-fixes

preen:	format lint

test:	preen
	pytest --verbose --cov-fail-under=$(COVERAGE) $(PROJECT)

report:	doc badge

doc:
	pdoc $(PROJECT) !$(PROJECT).tests --output-directory public/pdoc_docs
	pytest --cov --cov-report=html:public/coverage \
		--html=public/pytest_report.html --self-contained-html

badge:
	# pytest
	pytest --junitxml=public/pytest_report.xml
	genbadge tests --input-file public/pytest_report.xml --output-file public/tests.svg

clean:
	# clean generated artefacts
	$(RM) $(PROJECT)/__pycache__/ $(PROJECT)/*/__pycache__/
	$(RM) .coverage
	$(RM) .hypothesis/
	$(RM) .pytest_cache/
	$(RM) public/

cleanall: clean
    # clean development environment
	$(RM) .venv/
	$(RM) .idea/
	$(RM) requirements-dev.lock.txt

sync:
	@echo "Syncing environment from pyproject.toml (this will create .venv and uv.lock if needed)..."
	uv sync
	@echo "Environment '.venv' is ready and synced."
	@echo "To activate the virtual environment, run:"
	@echo "  source .venv/bin/activate          (*nix)"
	@echo "  .venv\\Scripts\\activate             (Windows)"