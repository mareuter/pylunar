# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2016, Michael Reuter
# Distributed under the MIT License. See LICENSE for more information.
# ------------------------------------------------------------------------------
import math
from operator import itemgetter

import ephem

from pylunar import mjd_to_date_tuple, tuple_to_string

__all__ = ["MoonInfo"]


class MoonInfo(object):
    """Handle all moon information.

    Attributes
    ----------
    observer : ephem.Observer instance.
        The instance containing the observer's location information.
    moon : ephem.Moon instance
        The instance of the moon object.
    """

    def __init__(self, latitude, longitude, name=None):
        """Initialize the class.

        Parameters
        ----------
        latitude : tuple of 3 ints
            The latitude of the observer.
        longitude : tuple of 3 ints
            The longitude of the observer.
        name : str, optional
            A name for the observer's location.
        """
        self.observer = ephem.Observer()
        self.observer.lat = tuple_to_string(latitude)
        self.observer.long = tuple_to_string(longitude)
        self.moon = ephem.Moon()

    def age(self):
        """The moon's age in days.

        Returns
        -------
        float
        """
        prev_new = ephem.previous_new_moon(self.observer.date)
        return self.observer.date - prev_new

    def altitude(self):
        """The moon's altitude in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.alt)

    def azimuth(self):
        """The moon's azimuth in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.az)

    def colong(self):
        """The moon's selenographic colongitude in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.colong)

    def fractional_phase(self):
        """The moon's fractional illumination. Always less than 1.0.

        Returns
        -------
        float
        """
        return self.moon.moon_phase

    def libration_lat(self):
        """The moon's current latitudinal libration in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.libration_lat)

    def libration_lon(self):
        """The moon's current longitudinal libration in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.libration_long)

    def next_four_phases(self):
        """The next for phases in date sorted order (closest phase first).

        Returns
        -------
        list[(str, float)]
            Set of moon phases specified by an abbreviated phase name and Modified Julian Date.
        """
        phases = {}
        phases["new"] = ephem.next_new_moon(self.observer.date)
        phases["fq"] = ephem.next_first_quarter_moon(self.observer.date)
        phases["full"] = ephem.next_full_moon(self.observer.date)
        phases["tq"] = ephem.next_last_quarter_moon(self.observer.date)

        sorted_phases = sorted(phases.items(), key=itemgetter(1))
        sorted_phases = [(phase[0], mjd_to_date_tuple(phase[1])) for phase in sorted_phases]

        return sorted_phases

    def update(self, datetime):
        """Update the moon information based on time.

        This fuction updates the Observer instance's datetime setting. The incoming datetime tuple should be
        in UTC with the following placement of values: (YYYY, m, d, H, M, S) as defined below::

            YYYY
                Four digit year

            m
                month (1-12)

            d
                day (1-31)

            H
                hours (0-23)

            M
                minutes (0-59)

            S
                seconds (0-59)

        Parameters
        ----------
        datetime : tuple
            The current UTC time in a tuple of numbers.
        """
        self.observer.date = datetime
        self.moon.compute(self.observer)
