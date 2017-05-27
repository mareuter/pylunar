# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2016-2017, Michael Reuter
# Distributed under the MIT License. See LICENSE for more information.
# ------------------------------------------------------------------------------
from __future__ import division
from datetime import datetime
from enum import Enum
import math
from operator import itemgetter

import ephem
import pytz

from pylunar import mjd_to_date_tuple, tuple_to_string

__all__ = ["MoonInfo"]

class PhaseName(Enum):
    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7

class TimeOfDay(Enum):
    MORNING = 0
    EVENING = 1

class MoonInfo(object):
    """Handle all moon information.

    Attributes
    ----------
    observer : ephem.Observer instance.
        The instance containing the observer's location information.
    moon : ephem.Moon instance
        The instance of the moon object.
    """

    DAYS_TO_HOURS = 24.0
    MAIN_PHASE_CUTOFF = 2.0
    # Time cutoff (hours) around the NM, FQ, FM, and LQ phases
    FEATURE_CUTOFF = 15.0
    # The offset (degrees) from the colongitude used for visibility check
    NO_CUTOFF_TYPE = ("Mare", "Oceanus")
    # Feature types that are not subject to longitude cutoffs

    reverse_phase_lookup = {
        "new_moon": (ephem.previous_last_quarter_moon, "last_quarter"),
        "first_quarter": (ephem.previous_new_moon, "new_moon"),
        "full_moon": (ephem.previous_first_quarter_moon, "first_quarter"),
        "last_quarter": (ephem.previous_full_moon, "full_moon")
    }

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

    def angular_size(self):
        """The moon's current angular size in degrees.

        Returns
        -------
        float
        """
        return self.moon.size / 3600.0

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

    def dec(self):
        """The moon's current declination in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.dec)

    def earth_distance(self):
        """The moon's current distance from the earth in km.

        Returns
        -------
        float
        """
        return self.moon.earth_distance * ephem.meters_per_au / 1000.0

    def elongation(self):
        """The moon's elongation from the sun in degrees.

        Returns
        -------
        float
        """
        elongation = math.degrees(self.moon.elong)
        if elongation < 0:
            elongation += 360.0
        return elongation

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

    def magnitude(self):
        """ The moon's current magnitude.

        Returns
        -------
        float
        """
        return self.moon.mag

    def colong_to_long(self):
        """The selenographic longitude in degrees based on the terminator.

        Returns
        -------
        float
        """
        colong = self.colong()
        if 90.0 <= colong < 270.0:
            longitude = 180.0 - colong
        elif 270.0 <= colong < 360.0:
            longitude = 360.0 - colong
        else:
            longitude = -colong

        return longitude

    def is_visible(self, feature):
        """Determine if lunar feature is visible.

        Parameters
        ----------
        feature : :class:`.LunarFeature`
            The Lunar feature instance to check.

        Returns
        -------
        bool
            True if visible, False if not.
        """
        selco_lon = self.colong_to_long()
        current_tod = self.time_of_day()

        min_lon = feature.longitude - feature.delta_longitude / 2
        max_lon = feature.longitude + feature.delta_longitude / 2

        if min_lon > max_lon:
            min_lon, max_lon = max_lon, min_lon

        is_visible = False
        latitude_scaling = math.cos(math.radians(feature.latitude))
        if feature.feature_type not in MoonInfo.NO_CUTOFF_TYPE:
            cutoff = MoonInfo.FEATURE_CUTOFF / latitude_scaling
        else:
            cutoff = MoonInfo.FEATURE_CUTOFF

        if current_tod == TimeOfDay.MORNING.name:
            # Minimum longitude for morning visibility
            lon_cutoff = min_lon - cutoff
            if feature.feature_type in MoonInfo.NO_CUTOFF_TYPE:
                is_visible = selco_lon <= min_lon
            else:
                is_visible = lon_cutoff <= selco_lon <= min_lon
        else:
            # Maximum longitude for evening visibility
            lon_cutoff = max_lon + cutoff
            if feature.feature_type in MoonInfo.NO_CUTOFF_TYPE:
                is_visible = max_lon <= selco_lon
            else:
                is_visible = max_lon <= selco_lon <= lon_cutoff

        return is_visible

    def next_four_phases(self):
        """The next for phases in date sorted order (closest phase first).

        Returns
        -------
        list[(str, float)]
            Set of moon phases specified by an abbreviated phase name and Modified Julian Date.
        """
        phases = {}
        phases["new_moon"] = ephem.next_new_moon(self.observer.date)
        phases["first_quarter"] = ephem.next_first_quarter_moon(self.observer.date)
        phases["full_moon"] = ephem.next_full_moon(self.observer.date)
        phases["last_quarter"] = ephem.next_last_quarter_moon(self.observer.date)

        sorted_phases = sorted(phases.items(), key=itemgetter(1))
        sorted_phases = [(phase[0], mjd_to_date_tuple(phase[1])) for phase in sorted_phases]

        return sorted_phases

    def phase_name(self):
        """The standard name of the moon's phase, i.e. Waxing Cresent

        This function returns a standard name for the moon's phase based on the current selenographic
        colongitude.

        Returns
        -------
        str
        """
        next_phase_name = self.next_four_phases()[0][0]
        try:
            next_phase_time = getattr(ephem, "next_{}".format(next_phase_name))(self.observer.date)
        except AttributeError:
            next_phase_time = getattr(ephem, "next_{}_moon".format(next_phase_name))(self.observer.date)
        previous_phase = self.reverse_phase_lookup[next_phase_name]
        time_to_next_phase = math.fabs(next_phase_time - self.observer.date) * self.DAYS_TO_HOURS
        time_to_previous_phase = math.fabs(self.observer.date -
                                           previous_phase[0](self.observer.date)) * self.DAYS_TO_HOURS
        previous_phase_name = previous_phase[1]

        if time_to_previous_phase < self.MAIN_PHASE_CUTOFF:
            return getattr(PhaseName, previous_phase_name.upper()).name
        elif time_to_next_phase < self.MAIN_PHASE_CUTOFF:
            return getattr(PhaseName, next_phase_name.upper()).name
        else:
            if previous_phase_name == "new_moon" and next_phase_name == "first_quarter":
                return PhaseName.WAXING_CRESCENT.name
            elif previous_phase_name == "first_quarter" and next_phase_name == "full_moon":
                return PhaseName.WAXING_GIBBOUS.name
            elif previous_phase_name == "full_moon" and next_phase_name == "last_quarter":
                return PhaseName.WANING_GIBBOUS.name
            elif previous_phase_name == "last_quarter" and next_phase_name == "new_moon":
                return PhaseName.WANING_CRESCENT.name

    def ra(self):
        """The moon's current right ascension in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.ra)

    def rise_set_times(self, timezone):
        """Calculate the rise, set and transit times in the local time system.

        Parameters
        ----------
        timezone : str
            The timezone identifier for the calculations.

        Returns
        -------
        list[(str, tuple)]
            Set of rise, set, and transit times in the local time system. If event
            does not happen, 'Does not xxx' is tuple value.
        """
        utc = pytz.utc
        try:
            tz = pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            tz = utc

        func_map = {"rise": "rising", "transit": "transit", "set": "setting"}

        # Need to set observer's horizon and pressure to get times
        old_pressure = self.observer.pressure
        old_horizon = self.observer.horizon

        self.observer.pressure = 0
        self.observer.horizon = "-0:34"

        current_date_utc = datetime(*mjd_to_date_tuple(self.observer.date,
                                                       round_off=True), tzinfo=utc)
        current_date = current_date_utc.astimezone(tz)
        current_day = current_date.day
        times = {}
        does_not = None
        for time_type in ("rise", "transit", "set"):
            mjd_time = getattr(self.observer,
                               "{}_{}".format("next",
                                              func_map[time_type]))(self.moon)
            utc_time = datetime(*mjd_to_date_tuple(mjd_time, round_off=True),
                                tzinfo=utc)
            local_date = utc_time.astimezone(tz)
            if local_date.day == current_day:
                times[time_type] = local_date
            else:
                mjd_time = getattr(self.observer,
                                   "{}_{}".format("previous",
                                                  func_map[time_type]))(self.moon)
                utc_time = datetime(*mjd_to_date_tuple(mjd_time, round_off=True),
                                    tzinfo=utc)
                local_date = utc_time.astimezone(tz)
                if local_date.day == current_day:
                    times[time_type] = local_date
                else:
                    does_not = (time_type, "Does not {}".format(time_type))

        # Return observer to previous state
        self.observer.pressure = old_pressure
        self.observer.horizon = old_horizon

        sorted_times = sorted(times.items(), key=itemgetter(1))
        sorted_times = [(xtime[0], xtime[1].timetuple()[:6]) for xtime in sorted_times]
        if does_not is not None:
            sorted_times.insert(0, does_not)

        return sorted_times

    def subsolar_lat(self):
        """The latitude in degress on the moon where the sun is overhead.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.subsolar_lat)

    def time_of_day(self):
        """Determine if the terminator is sunrise (morning) or sunset (evening).

        Returns
        -------
        float
        """
        colong = self.colong()
        if 90.0 <= colong < 270.0:
            return TimeOfDay.EVENING.name
        else:
            return TimeOfDay.MORNING.name

    def time_from_new_moon(self):
        """The time (hours) from the previous new moon.

        This function calculates the time from the previous new moon.

        Returns
        -------
        float
        """
        previous_new_moon = ephem.previous_new_moon(self.observer.date)
        return MoonInfo.DAYS_TO_HOURS * (self.observer.date - previous_new_moon)

    def time_to_full_moon(self):
        """The time (days) to the next full moon.

        This function calculates the time to the next full moon.

        Returns
        -------
        float
        """
        next_full_moon = ephem.next_full_moon(self.observer.date)
        return next_full_moon - self.observer.date

    def time_to_new_moon(self):
        """The time (hours) to the next new moon.

        This function calculates the time to the next new moon.

        Returns
        -------
        float
        """
        next_new_moon = ephem.next_new_moon(self.observer.date)
        return MoonInfo.DAYS_TO_HOURS * (next_new_moon - self.observer.date)

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
