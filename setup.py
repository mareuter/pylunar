#!/usr/bin/env python

# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

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

requirements = None
with open('requirements/prod.txt') as prodFile:
    requirements = [x.strip() for x in prodFile]

test_requirements = None
with open('requirements/test.txt') as testFile:
    test_requirements = [x.strip() for x in testFile]

setup(
    name='pylunar',
    version='0.5.1',
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
    license='BSD 3-Clause License',
    zip_safe=False,
    keywords='pylunar',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
