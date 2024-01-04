.PHONY: help check-build clean clean-pyc clean-build clean-docs list test test-all coverage docs release sdist

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-docs - remove doc build artifacts"
	@echo "clean - remove all artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "check-build - check distribution packaging"

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
	flake8 pylunar tests

test:
	pytest -v --doctest-glob=docs/usage.rst

test-all: test

coverage:
	coverage run --source pylunar setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: clean-docs
	sphinx-apidoc -fMeT -o docs/api src/pylunar
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

sdist: clean
	python setup.py sdist
	python setup.py bdist_wheel upload
	ls -l dist

check-build: clean
	python -m build
	twine check dist/*
