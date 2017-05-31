#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://pylunar.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    "ephem",
    "pytz"
]

test_requirements = [
    "wheel>=0.22",
    "bumpversion",
    "flake8",
    "tox",
    "coverage",
    "Sphinx",
    "cryptography",
    "PyYAML"
]

setup(
    name='pylunar',
    version='0.4.1',
    description='Information for completing the Astronomical League\'s ' +
                'Lunar and Lunar II observing programs.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Michael Reuter',
    author_email='mareuternh@gmail.com',
    url='https://github.com/mareuter/pylunar',
    packages=[
        'pylunar',
    ],
    package_dir={'pylunar': 'pylunar'},
    include_package_data=True,
    install_requires=requirements,
    extras_require={':python_version=="2.7"': ['enum34']},
    license='MIT',
    zip_safe=False,
    keywords='pylunar',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='tests',
    tests_require=test_requirements

)
