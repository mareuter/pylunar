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

from typing import List, TypeAlias, Union

DateTimeTuple: TypeAlias = tuple[int, int, int, int, int, Union[int, float]]
MoonPhases: TypeAlias = List[tuple[str, Union[DateTimeTuple, str]]]
DmsCoordinate: TypeAlias = tuple[int, int, int]
Range: TypeAlias = tuple[float, float]
LunarFeatureList: TypeAlias = tuple[str, float, float, float, float, float, str, str, str, str, str | None]
FeatureRow: TypeAlias = tuple[int, str, float, float, float, float, float, str, str, str, str, str]
