# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2016, Michael Reuter
# Distributed under the MIT License. See LICENSE for more information.
# ------------------------------------------------------------------------------
import collections
import pkg_resources
import sqlite3

from pylunar import LunarFeature


class LunarFeatureContainer(object):

    """
    This class handles collecting all of the Lunar features that are available from the
    database.
    """

    def __init__(self, club_name):
        """Initialize the class.

        Parameters
        ----------
        club_name : str
            The name of the observing club to sort on. Values are Lunar and LunarII.
        """
        rsman = pkg_resources.ResourceManager()
        dbname = rsman.resource_filename('pylunar', 'db/lunar.db')
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
        for feature in self.features.values():
            yield feature

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
        sql = "select * from Features where Lunar_Code = \"{}\" or "\
              "Lunar_Code = \"Both\"".format(self.club_name)
        if limit is not None:
            sql += " limit {}".format(limit)
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
