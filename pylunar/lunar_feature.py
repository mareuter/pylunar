# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

import math
import os

__all__ = ["LunarFeature"]


class LunarFeature(object):

    """
    This class handles keeping all the information for a given Lunar feature.
    """

    def __init__(self, name, diameter, latitude, longitude,
                 delta_latitude, delta_longitude, feature_type,
                 quad_name, quad_code, code_name,
                 lunar_club_type):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name of the Lunar feature (no unicode)
        diameter : float
            The diameter (km) of the Lunar feature.
        latitude : float
            The latitude (degrees) of the Lunar feature. Negative is South, positive is North.
        longitude : float
            The longitude (degrees) of the Lunar feature. Negative is West, positive is East
        delta_latitude : float
            The size (degrees) in latitude of the Lunar feature.
        delta_longitude : float
            The size (degrees) in longitude of the Lunar feature.
        feature_type : str
            The classification of the Lunar feature: i.e. Crater, Mons.
        quad_name : str
            Name of lunar quadrant containing feature's center point as determined
            by the International Astronomical Union (IAU) Working Group for
            Planetary System Nomenclature (WGPSN)
        quad_code : str
            Specific lunar quadrant containing feature's center point as determined
            by the IAU WGPSN.
        code_name : str
            The AstroLeague club name for the Lunar feature. Can be: Lunar, LunarII or Both
        lunar_club_type : str or None
            The Lunar Club classification of the feature: Naked Eye, Binocular, Telescope.
            For a LunarII only feature this is None.
        """

        self.name = name
        self.diameter = diameter
        self.latitude = latitude
        self.longitude = longitude
        self.delta_latitude = delta_latitude
        self.delta_longitude = delta_longitude
        self.feature_type = feature_type
        self.quad_name = quad_name
        self.quad_code = quad_code
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
        result.append("Lat/Long = ({:.2f}, {:.2f})".format(self.latitude, self.longitude))
        result.append("Type = {}".format(self.feature_type))
        result.append("Delta Lat/Long = ({:.2f}, {:.2f})".format(self.delta_latitude, self.delta_longitude))
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
        return cls(*row[1:])

    def feature_angle(self):
        """Get the angle of the feature on the lunar face relative to North.

        The feature angle is determined by calculating atan2(lon, lat) and
        then adding 360 degrees if the result is less than zero. This makes
        North zero degrees, East 90 degrees, South 180 degrees and West 270
        degrees.

        Returns
        -------
        float
            The feature angle in degrees.
        """
        lat_rad = math.radians(self.latitude)
        lon_rad = math.radians(self.longitude)
        fa = math.degrees(math.atan2(lon_rad, lat_rad))
        fa += 360.0 if fa < 0 else 0.0
        return fa

    def latitude_range(self):
        """Get the latitude range of the feature.

        Returns
        -------
        tuple(float, float)
            The (minimum, maximum) latitude values for the feature.
        """
        min_lat = self.latitude - (self.delta_latitude / 2.0)
        max_lat = self.latitude + (self.delta_latitude / 2.0)
        return (min_lat, max_lat)

    def list_from_feature(self):
        """list: Convert the feature information into a list.
        """
        return [self.name, self.diameter, self.latitude, self.longitude,
                self.delta_latitude, self.delta_longitude, self.feature_type,
                self.quad_name, self.quad_code, self.code_name,
                self.lunar_club_type]

    def longitude_range(self):
        """Get the longitude range of the feature.

        Returns
        -------
        tuple(float, float)
            The (minimum, maximum) longitude values for the feature.
        """
        min_lon = self.longitude - (self.delta_longitude / 2.0)
        max_lon = self.longitude + (self.delta_longitude / 2.0)
        return (min_lon, max_lon)
