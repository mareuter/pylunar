# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Module for the LunarFeature class."""

from __future__ import annotations

__all__ = ["LunarFeature"]

import math
import os

from .pkg_types import FeatureRow, Range


class LunarFeature:
    """Class keeping all the information for a given Lunar feature.

    Parameters
    ----------
    name : str
        The name of the Lunar feature (no unicode).
    diameter : float
        The diameter (km) of the Lunar feature.
    latitude : float
        The latitude (degrees) of the Lunar feature. Negative is South,
        positive is North.
    longitude : float
        The longitude (degrees) of the Lunar feature. Negative is West,
        positive is East.
    delta_latitude : float
        The size (degrees) in latitude of the Lunar feature.
    delta_longitude : float
        The size (degrees) in longitude of the Lunar feature.
    feature_type : str
        The classification of the Lunar feature: i.e. Crater, Mons.
    quad_name : str
        Name of lunar quadrant containing feature's center point as
        determined by the International Astronomical Union (IAU) Working
        Group for Planetary System Nomenclature (WGPSN).
    quad_code : str
        Specific lunar quadrant containing feature's center point as
        determined by the IAU WGPSN.
    code_name : str
        The AstroLeague club name for the Lunar feature. Can be: Lunar,
        LunarII or Both.
    lunar_club_type : str or None
        The Lunar Club classification of the feature: Naked Eye, Binocular,
        Telescope. For a LunarII only feature this is None.
    """

    def __init__(
        self,
        name: str,
        diameter: float,
        latitude: float,
        longitude: float,
        delta_latitude: float,
        delta_longitude: float,
        feature_type: str,
        quad_name: str,
        quad_code: str,
        code_name: str,
        lunar_club_type: str | None,
    ):
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

    def __str__(self) -> str:
        """Class string representation.

        Returns
        -------
        str
            The string representation.
        """
        result = []
        result.append(f"Name = {self.name}")
        result.append(f"Lat/Long = ({self.latitude:.2f}, {self.longitude:.2f})")
        result.append(f"Type = {self.feature_type}")
        result.append(f"Delta Lat/Long = ({self.delta_latitude:.2f}, {self.delta_longitude:.2f})")
        return os.linesep.join(result)

    @classmethod
    def from_row(cls: type[LunarFeature], row: FeatureRow) -> LunarFeature:
        """Initialize from a database row.

        Parameters
        ----------
        row : list
            The database row containing the information.

        Returns
        -------
        :class:`.LunarFeature`
            Class initialized from database row.
        """
        return cls(*row[1:])

    def feature_angle(self) -> float:
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

    def latitude_range(self) -> Range:
        """Get the latitude range of the feature.

        Returns
        -------
        tuple(float, float)
            The (minimum, maximum) latitude values for the feature.
        """
        min_lat = self.latitude - (self.delta_latitude / 2.0)
        max_lat = self.latitude + (self.delta_latitude / 2.0)
        return (min_lat, max_lat)

    def list_from_feature(self) -> list[object]:
        """Convert the feature information into a list.

        Returns
        -------
        list
            The list of lunar features.
        """
        return [
            self.name,
            self.diameter,
            self.latitude,
            self.longitude,
            self.delta_latitude,
            self.delta_longitude,
            self.feature_type,
            self.quad_name,
            self.quad_code,
            self.code_name,
            self.lunar_club_type,
        ]

    def longitude_range(self) -> Range:
        """Get the longitude range of the feature.

        Returns
        -------
        tuple(float, float)
            The (minimum, maximum) longitude values for the feature.
        """
        min_lon = self.longitude - (self.delta_longitude / 2.0)
        max_lon = self.longitude + (self.delta_longitude / 2.0)
        return (min_lon, max_lon)
