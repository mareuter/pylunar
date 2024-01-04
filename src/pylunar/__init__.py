# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

from importlib.metadata import version, PackageNotFoundError

__author__ = 'Michael Reuter'
__email__ = 'mareuternh@gmail.com'
try:
    __version__ = version("pylunar")
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"

version_info = __version__.split(".")
"""The decomposed version, split across "``.``."

Use this for version comparison.
"""

from .helpers import *
from .lunar_feature import LunarFeature
from .lunar_feature_container import LunarFeatureContainer
from .moon_info import MoonInfo
