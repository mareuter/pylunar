.PHONY: help
help:
	@echo "check-build - check distribution packaging"
	@echo "clean-build - remove build artifacts"
	@echo "clean-docs - remove doc build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean - remove all artifacts"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs-local - generate docs and open locally"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "init - initialize a clean clone"
	@echo "lint - check style with ruff"
	@echo "release - package and upload a release"
	@echo "test - run tests quickly with the default Python"
	@echo "update-deps" - update dependencies"
	@echo "update-precommit - update pre-commit config"
	@echo "update" - update dependencies and pre-commit config

.PHONY: check-build
check-build: clean
	uv build
	twine check dist/*

.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr src/*.egg-info

.PHONY: clean-docs
clean-docs:
	rm -fr docs/api
	$(MAKE) -C docs clean

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

.PHONY: clean
clean: clean-build clean-docs clean-pyc

.PHONY: coverage
coverage:
	coverage run -m pytest
	coverage report -m
	coverage html
	open htmlcov/index.html

.PHONY: doc-local
docs-local: docs
	open docs/_build/html/index.html

.PHONY: docs
docs: clean-docs
	sphinx-apidoc -fMeT -o docs/api src/pylunar
	$(MAKE) -C docs html

.PHONY: init
init:
	uv sync --frozen --all-groups
	uv run prek install
	mkdir -p changelog.d

.PHONY: lint
lint:
	tox -e lint

.PHONY: release
release: clean
	uv build
	uv publish

.PHONY: test
test:
	pytest -v --doctest-glob=docs/usage.rst

.PHONY: update-deps
update-deps: update-precommit
	uv lock --upgrade

.PHONY: update-precommit
update-precommit:
	uv run --only-group=lint prek autoupdate

.PHONY: update
update: update-deps init
