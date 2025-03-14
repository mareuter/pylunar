# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Module for holding types."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from typing import Union

DateTimeTuple: TypeAlias = Union[tuple[int, ...], tuple[int, int, int, int, int, float]]
MoonPhases: TypeAlias = list[tuple[str, Union[DateTimeTuple, str]]]
DmsCoordinate: TypeAlias = tuple[int, int, int]
Range: TypeAlias = tuple[float, float]
LunarFeatureList: TypeAlias = tuple[
    str, float, float, float, float, float, str, str, str, str, Union[str, None]
]
FeatureRow: TypeAlias = tuple[int, str, float, float, float, float, float, str, str, str, str, str]
