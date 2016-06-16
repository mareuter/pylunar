# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2016, Michael Reuter
# Distributed under the MIT License. See LICENSE for more information.
# ------------------------------------------------------------------------------
import pkg_resources
import sqlite3

from pylunar import LunarFeature


class LunarFeatureContainer(object):

    """
    This class handles collecting all of the Lunar features that are available from the
    database.
    """

    def __init__(self):
        """Initialize the class.
        """
        rsman = pkg_resources.ResourceManager()
        dbname = rsman.resource_filename('pylunar', 'db/lunar.db')
        self.conn = sqlite3.connect(dbname)
        self.features = {}
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

    def load(self, limit=None):
        """Read the Lunar features from the database.

        Parameters
        ----------
        limit : int, optional
            Restrict the number of features read to the given value.
        """
        if len(self.features) != 0:
            self.features = {}

        cur = self.conn.cursor()
        sql = "select * from Features"
        if limit is not None:
            sql += " limit {}".format(limit)
        cur.execute(sql)

        for row in cur:
            feature = LunarFeature.from_row(row)
            self.features[id(feature)] = feature
            self.club_type.add(row[11])
            self.feature_type.add(row[7])

        cur.close()
