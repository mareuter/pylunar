.PHONY: help init clean-pyc clean-build clean-docs clean lint test coverage docs docs-local release check-build

help:
	@echo "init - initialize a clean clone"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-docs - remove doc build artifacts"
	@echo "clean - remove all artifacts"
	@echo "lint - check style with ruff"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "docs-local - generate docs and open locally"
	@echo "release - package and upload a release"
	@echo "check-build - check distribution packaging"

init:
	pip install --editable .[dev]
	pre-commit install

clean: clean-build clean-docs clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr src/*.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-docs:
	rm -fr docs/api
	$(MAKE) -C docs clean

lint:
	tox -e lint

test:
	pytest -v --doctest-glob=docs/usage.rst

coverage:
	coverage run -m pytest
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: clean-docs
	sphinx-apidoc -fMeT -o docs/api src/pylunar
	$(MAKE) -C docs html

docs-local: docs
	open docs/_build/html/index.html

release: clean
	python -m build
	twine upload dist/*

check-build: clean
	python -m build
	twine check dist/*
