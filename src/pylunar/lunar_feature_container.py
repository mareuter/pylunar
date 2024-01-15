# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Module for the LunarFeatureContainer class."""

__all__ = ["LunarFeatureContainer"]

import collections

try:
    from importlib_resources import files
except ImportError:
    from importlib.resources import files
import sqlite3

from .lunar_feature import LunarFeature


class LunarFeatureContainer:
    """Collection of Lunar features available from the database."""

    def __init__(self, club_name):
        """Initialize the class.

        Parameters
        ----------
        club_name : str
            The name of the observing club to sort on. Values are Lunar and
            LunarII.
        """
        dbname = files("pylunar.data").joinpath("lunar.db")
        self.conn = sqlite3.connect(dbname)
        self.club_name = club_name
        self.features = collections.OrderedDict()
        self.club_type = set()
        self.feature_type = set()

    def __iter__(self):
        """Create iterator for container.

        Returns
        -------
        :class:`.LunarFeature`
        """
        yield from self.features.values()

    def __len__(self):
        """Length of the container.

        Returns
        -------
        int
        """
        return len(self.features)

    def load(self, moon_info=None, limit=None):
        """Read the Lunar features from the database.

        Parameters
        ----------
        moon_info : :class:`.MoonInfo`, optional
            Instance of the Lunar information class.
        limit : int, optional
            Restrict the number of features read to the given value.
        """
        if len(self.features) != 0:
            self.features = collections.OrderedDict()

        cur = self.conn.cursor()
        sql = f'select * from Features where Lunar_Code = "{self.club_name}" or ' 'Lunar_Code = "Both"'
        if limit is not None:
            sql += f" limit {limit}"
        cur.execute(sql)

        for row in cur:
            feature = LunarFeature.from_row(row)
            try:
                is_visible = moon_info.is_visible(feature)
            except AttributeError:
                is_visible = True
            if is_visible:
                self.features[id(feature)] = feature
                self.club_type.add(row[11])
                self.feature_type.add(row[7])

        cur.close()
