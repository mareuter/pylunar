# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Module for the AltitudeDict class."""

from __future__ import annotations

import sys
from typing import Dict

if sys.version_info >= (3, 10):
    from importlib.resources import files
else:
    from importlib_resources import files

import sqlite3

from .lunar_feature import LunarFeature
from .moon_info import MoonInfo

__all__ = ["AltitudeDict"]


class AltitudeDict(Dict[str, float]):
    """Dictionary for the Lunar II features requiring solar altitude."""

    def load(self, moon_info: MoonInfo) -> None:
        """Provide solar altitude for the Lunar II features.

        Parameters
        ----------
        moon_info : :class:`pylunar.MoonInfo`
            Instance of the Lunar information class.
        """
        features = ["Byrgius A", "Proclus", "Rupes Recta", "Tycho"]
        dbname = str(files("pylunar.data").joinpath("lunar.db"))
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()

        sql = f"select * from Features where Name in {str(tuple(features))}"
        cur.execute(sql)

        feature_list = []
        for row in cur:
            feature_list.append(LunarFeature.from_row(row))

        for feature in sorted(feature_list, key=lambda x: x.name):
            self[feature.name] = moon_info.solar_altitude(feature)

        cur.close()
