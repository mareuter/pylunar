# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2016, Michael Reuter
# Distributed under the MIT License. See LICENSE for more information.
# ------------------------------------------------------------------------------
import os

__all__ = ["LunarFeature"]


class LunarFeature(object):

    """
    This class handles keeping all the information for a given Lunar feature.
    """

    def __init__(self, name, latitude, longitude, feature_type,
                 delta_latitude, delta_longitude, code_name, lunar_club_type):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name of the Lunar feature (no unicode)
        latitude : float
            The latitude (degrees) of the Lunar feature. Negative is South, positive is North.
        longitude : float
            The longitude (degrees) of the Lunar feature. Negative is West, positive is East
        feature_type : str
            The classification of the Lunar feature: i.e. Crater, Mons.
        delta_latitude : float
            The size (degrees) in latitude of the Lunar feature.
        delta_longitude : float
            The size (degrees) in longitude of the Lunar feature.
        code_name : str
            The AstroLeague club name for the Lunar feature. Can be: Lunar, LunarII or Both
        lunar_club_type : str or None
            The Lunar Club classification of the feature: Naked Eye, Binocular, Telescope.
            For a LunarII only feature this is None.
        """

        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.feature_type = feature_type
        self.delta_latitude = delta_latitude
        self.delta_longitude = delta_longitude
        self.code_name = code_name
        self.lunar_club_type = str(lunar_club_type)

    def __str__(self):
        """The string representation of the class.

        Returns
        -------
        str
        """
        result = []
        result.append("Name = {}".format(self.name))
        result.append("Lat/Long = ({:.2}, {:.2})".format(self.latitude, self.longitude))
        result.append("Type = {}".format(self.feature_type))
        result.append("Delta Lat/Long = ({:.2}, {:.2})".format(self.delta_latitude, self.delta_longitude))
        return os.linesep.join(result)

    @classmethod
    def from_row(cls, row):
        """Initialize from a database row.

        Parameters
        ----------
        row : list
            The database row containing the information.

        Returns
        -------
        :class:`.LunarFeature`
        """
        return cls(row[1], row[3], row[4], row[7], row[5], row[6], row[10], row[11])
