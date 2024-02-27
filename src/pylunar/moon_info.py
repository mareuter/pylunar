# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Module for the MoonInfo class."""

from __future__ import annotations

__all__ = ["MoonInfo"]

from datetime import datetime
from enum import Enum
import math
from operator import itemgetter

import ephem
import pytz

from .helpers import mjd_to_date_tuple, tuple_to_string
from .lunar_feature import LunarFeature
from .pkg_types import DateTimeTuple, DmsCoordinate, MoonPhases


class PhaseName(Enum):
    """Phase names for the lunar cycle."""

    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7


class TimeOfDay(Enum):
    """Time of day from the lunar terminator."""

    MORNING = 0
    EVENING = 1


class MoonInfo:
    """Handle all moon information.

    Attributes
    ----------
    observer : ephem.Observer instance.
        The instance containing the observer's location information.
    moon : ephem.Moon instance
        The instance of the moon object.

    Parameters
    ----------
    latitude : tuple of 3 ints
        The latitude of the observer in GPS DMS(Degrees, Minutes and
        Seconds) format.
    longitude : tuple of 3 ints
        The longitude of the observer in GPS DMS(Degrees, Minutes and
        Seconds) format.
    name : str, optional
        A name for the observer's location.
    """

    DAYS_TO_HOURS = 24.0
    MAIN_PHASE_CUTOFF = 2.0
    # Time cutoff (hours) around the NM, FQ, FM, and LQ phases
    FEATURE_CUTOFF = 15.0
    # The offset (degrees) from the colongitude used for visibility check
    NO_CUTOFF_TYPE = ("Landing Site", "Mare", "Oceanus")
    # Feature types that are not subject to longitude cutoffs
    LIBRATION_ZONE = 80.0
    # Latitude and/or longitude where librations have a big effect
    MAXIMUM_LIBRATION_PHASE_ANGLE_CUTOFF = 65.0
    # The maximum value of the libration phase angle difference for a feature

    reverse_phase_lookup = {
        "new_moon": (ephem.previous_last_quarter_moon, "last_quarter"),
        "first_quarter": (ephem.previous_new_moon, "new_moon"),
        "full_moon": (ephem.previous_first_quarter_moon, "first_quarter"),
        "last_quarter": (ephem.previous_full_moon, "full_moon"),
    }

    def __init__(self, latitude: DmsCoordinate, longitude: DmsCoordinate, name: str | None = None):
        self.observer = ephem.Observer()
        self.observer.lat = tuple_to_string(latitude)
        self.observer.long = tuple_to_string(longitude)
        self.moon = ephem.Moon()

    def age(self) -> float:
        """Lunar age in days.

        Returns
        -------
        float
            The lunar age.
        """
        prev_new = ephem.previous_new_moon(self.observer.date)
        return float(self.observer.date - prev_new)

    def fractional_age(self) -> float:
        """Lunar fractional age which is always less than 1.0.

        Returns
        -------
        float
            The fractional lunar age.
        """
        prev_new = ephem.previous_new_moon(self.observer.date)
        next_new = ephem.next_new_moon(self.observer.date)
        return float((self.observer.date - prev_new) / (next_new - prev_new))

    def altitude(self) -> float:
        """Lunar altitude in degrees.

        Returns
        -------
        float
            The lunar altitiude.
        """
        return math.degrees(self.moon.alt)

    def angular_size(self) -> float:
        """Lunar current angular size in degrees.

        Returns
        -------
        float
            The lunar angular size.
        """
        moon_size: float = self.moon.size
        return moon_size / 3600.0

    def azimuth(self) -> float:
        """Lunar azimuth in degrees.

        Returns
        -------
        float
            The lunar azimuth.
        """
        return math.degrees(self.moon.az)

    def colong(self) -> float:
        """Lunar selenographic colongitude in degrees.

        Returns
        -------
        float
            The lunar seleographic colongitude.
        """
        return math.degrees(self.moon.colong)

    def dec(self) -> float:
        """Lunar current declination in degrees.

        Returns
        -------
        float
            The lunar declination.
        """
        return math.degrees(self.moon.dec)

    def earth_distance(self) -> float:
        """Lunar current distance from the earth in km.

        Returns
        -------
        float
            THe earth-moon distance.
        """
        return float(self.moon.earth_distance * ephem.meters_per_au / 1000.0)

    def elongation(self) -> float:
        """Lunar elongation from the sun in degrees.

        Returns
        -------
        float
            The lunar solar elongation.
        """
        elongation = math.degrees(self.moon.elong)
        if elongation < 0:
            elongation += 360.0
        return elongation

    def fractional_phase(self) -> float:
        """Lunar fractional illumination which is always less than 1.0.

        Returns
        -------
        float
            The lunar fractional phase.
        """
        return float(self.moon.moon_phase)

    def libration_lat(self) -> float:
        """Lunar current latitudinal libration in degrees.

        Returns
        -------
        float
            The lunar libration latitude.
        """
        return math.degrees(self.moon.libration_lat)

    def libration_lon(self) -> float:
        """Lunar current longitudinal libration in degrees.

        Returns
        -------
        float
            The lunar libration longitude.
        """
        return math.degrees(self.moon.libration_long)

    def libration_phase_angle(self) -> float:
        """Phase angle of lunar current libration in degrees.

        Returns
        -------
        float
            The lunar libration phase angle.
        """
        phase_angle = math.atan2(self.moon.libration_long, self.moon.libration_lat)
        phase_angle += 2.0 * math.pi if phase_angle < 0 else 0.0
        return math.degrees(phase_angle)

    def magnitude(self) -> float:
        """Lunar current magnitude.

        Returns
        -------
        float
            The lunar magnitude.
        """
        return float(self.moon.mag)

    def colong_to_long(self) -> float:
        """Selenographic longitude in degrees based on the terminator.

        Returns
        -------
        float
            The lunar seleographic longitude.
        """
        colong: float = self.colong()
        if 90.0 <= colong < 270.0:
            longitude = 180.0 - colong
        elif 270.0 <= colong < 360.0:
            longitude = 360.0 - colong
        else:
            longitude = -colong

        return longitude

    def is_libration_ok(self, feature: LunarFeature) -> bool:
        """Determine if lunar feature is visible due to libration effect.

        Parameters
        ----------
        feature : :class:`.LunarFeature`
            The lunar feature instance to check.

        Returns
        -------
        bool
            True if visible, False if not.
        """
        is_lon_in_zone = math.fabs(feature.longitude) > self.LIBRATION_ZONE
        is_lat_in_zone = math.fabs(feature.latitude) > self.LIBRATION_ZONE
        if is_lat_in_zone or is_lon_in_zone:
            feature_angle = feature.feature_angle()
            libration_phase_angle = self.libration_phase_angle()
            delta_phase_angle = libration_phase_angle - feature_angle
            delta_phase_angle -= 360.0 if delta_phase_angle > 180.0 else 0.0

            return math.fabs(delta_phase_angle) <= self.MAXIMUM_LIBRATION_PHASE_ANGLE_CUTOFF

        return True

    def is_visible(self, feature: LunarFeature) -> bool:
        """Determine if lunar feature is visible.

        Parameters
        ----------
        feature : :class:`.LunarFeature`
            The lunar feature instance to check.

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

        return is_visible and self.is_libration_ok(feature)

    def next_four_phases(self) -> MoonPhases:
        """Next four phases in date sorted order (closest phase first).

        Returns
        -------
        list[(str, float)]
            Set of lunar phases specified by an abbreviated phase name and
            Modified Julian Date.
        """
        phases = {}
        phases["new_moon"] = ephem.next_new_moon(self.observer.date)
        phases["first_quarter"] = ephem.next_first_quarter_moon(self.observer.date)
        phases["full_moon"] = ephem.next_full_moon(self.observer.date)
        phases["last_quarter"] = ephem.next_last_quarter_moon(self.observer.date)

        sorted_phases = sorted(phases.items(), key=itemgetter(1))
        sorted_phases = [(phase[0], mjd_to_date_tuple(phase[1])) for phase in sorted_phases]

        return sorted_phases

    def phase_name(self) -> str:
        """Return standard name of lunar phase, i.e. Waxing Cresent.

        This function returns a standard name for lunar phase based on the
        current selenographic colongitude.

        Returns
        -------
        str
            The lunar phase name.
        """
        next_phase_name = self.next_four_phases()[0][0]
        try:
            next_phase_time = getattr(ephem, f"next_{next_phase_name}")(self.observer.date)
        except AttributeError:
            next_phase_time = getattr(ephem, f"next_{next_phase_name}_moon")(self.observer.date)
        previous_phase = self.reverse_phase_lookup[next_phase_name]
        time_to_next_phase = math.fabs(next_phase_time - self.observer.date) * self.DAYS_TO_HOURS
        time_to_previous_phase = (
            math.fabs(self.observer.date - previous_phase[0](self.observer.date)) * self.DAYS_TO_HOURS
        )
        previous_phase_name = previous_phase[1]

        phase_name = ""
        if time_to_previous_phase < self.MAIN_PHASE_CUTOFF:
            phase_name = getattr(PhaseName, previous_phase_name.upper()).name
        elif time_to_next_phase < self.MAIN_PHASE_CUTOFF:
            phase_name = getattr(PhaseName, next_phase_name.upper()).name
        else:
            if previous_phase_name == "new_moon" and next_phase_name == "first_quarter":
                phase_name = PhaseName.WAXING_CRESCENT.name
            elif previous_phase_name == "first_quarter" and next_phase_name == "full_moon":
                phase_name = PhaseName.WAXING_GIBBOUS.name
            elif previous_phase_name == "full_moon" and next_phase_name == "last_quarter":
                phase_name = PhaseName.WANING_GIBBOUS.name
            elif previous_phase_name == "last_quarter" and next_phase_name == "new_moon":
                phase_name = PhaseName.WANING_CRESCENT.name
        return phase_name

    def phase_shape_in_ascii(self) -> str:
        """Display lunar phase shape in ASCII art.

        This function returns a multi-line string demonstrate current lunar
        shape in ASCII format.

        Returns
        -------
        str
            The lunar phase shape.
        """
        phase = self.phase_name()

        if phase == PhaseName.NEW_MOON.name:
            return """   _..._
 .:::::::.
:::::::::::
:::::::::::
`:::::::::'
  `':::''        """
        elif phase == PhaseName.WAXING_CRESCENT.name:
            return """   _..._
 .::::. `.
:::::::.  :
::::::::  :
`::::::' .'
  `'::'-'        """
        elif phase == PhaseName.FIRST_QUARTER.name:
            return """   _..._
 .::::  `.
::::::    :
::::::    :
`:::::   .'
  `'::.-'        """
        elif phase == PhaseName.WAXING_GIBBOUS.name:
            return """   _..._
 .::'   `.
:::       :
:::       :
`::.     .'
  `':..-'        """
        elif phase == PhaseName.FULL_MOON.name:
            return """   _..._
 .'     `.
:         :
:         :
`.       .'
  `-...-'        """
        elif phase == PhaseName.WANING_GIBBOUS.name:
            return """   _..._
 .'   `::.
:       :::
:       :::
`.     .::'
  `-..:''        """
        elif phase == PhaseName.LAST_QUARTER.name:
            return """   _..._
 .'  ::::.
:    ::::::
:    ::::::
`.   :::::'
  `-.::''        """
        elif phase == PhaseName.WAXING_CRESCENT.name:
            return """   _..._
 .' .::::.
:  ::::::::
:  ::::::::
`. '::::::'
  `-.::''        """
        else:
            return phase

    def phase_emoji(self) -> str:
        """Return standard emoji of lunar phase, i.e. '🌒'.

        This function returns a standard emoji for lunar phase based on the
        current selenographic colongitude.

        Returns
        -------
        str
            The lunar phase emoji.
        """
        return {
            "NEW_MOON": "🌑",
            "WAXING_CRESCENT": "🌒",
            "FIRST_QUARTER": "🌓",
            "WAXING_GIBBOUS": "🌔",
            "FULL_MOON": "🌕",
            "WANING_GIBBOUS": "🌖",
            "LAST_QUARTER": "🌗",
            "WANING_CRESCENT": "🌘",
        }[self.phase_name()]

    def ra(self) -> float:
        """Lunar current right ascension in degrees.

        Returns
        -------
        float
            The lunar right ascension.
        """
        return math.degrees(self.moon.ra)

    def rise_set_times(self, timezone: str) -> MoonPhases:
        """Calculate the rise, set and transit times in the local time system.

        Parameters
        ----------
        timezone : str
            The timezone identifier for the calculations.

        Returns
        -------
        list[(str, tuple)]
            Set of rise, set, and transit times in the local time system. If
            event does not happen, 'Does not xxx' is tuple value.
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

        current_date_utc = datetime(*mjd_to_date_tuple(self.observer.date, round_off=True), tzinfo=utc)  # type: ignore
        current_date = current_date_utc.astimezone(tz)
        current_day = current_date.day
        times = {}
        does_not = None
        for time_type in ("rise", "transit", "set"):
            mjd_time = getattr(self.observer, "{}_{}".format("next", func_map[time_type]))(self.moon)
            utc_time = datetime(*mjd_to_date_tuple(mjd_time, round_off=True), tzinfo=utc)  # type: ignore
            local_date = utc_time.astimezone(tz)
            if local_date.day == current_day:
                times[time_type] = local_date
            else:
                mjd_time = getattr(self.observer, "{}_{}".format("previous", func_map[time_type]))(self.moon)
                utc_time = datetime(*mjd_to_date_tuple(mjd_time, round_off=True), tzinfo=utc)  # type: ignore
                local_date = utc_time.astimezone(tz)
                if local_date.day == current_day:
                    times[time_type] = local_date
                else:
                    does_not = (time_type, f"Does not {time_type}")

        # Return observer and moon to previous state
        self.observer.pressure = old_pressure
        self.observer.horizon = old_horizon
        self.moon.compute(self.observer)

        original_sorted_times = sorted(times.items(), key=itemgetter(1))
        sorted_times: MoonPhases = [(xtime[0], xtime[1].timetuple()[:6]) for xtime in original_sorted_times]
        if does_not is not None:
            sorted_times.insert(0, does_not)

        return sorted_times

    def subsolar_lat(self) -> float:
        """Latitude in degress on the moon where the sun is overhead.

        Returns
        -------
        float
            The lunar subsolar latitude.
        """
        return math.degrees(self.moon.subsolar_lat)

    def time_of_day(self) -> str:
        """Terminator time of day.

        This function determines if the terminator is sunrise (morning) or
        sunset (evening).

        Returns
        -------
        str
            The lunar time of day.
        """
        colong = self.colong()
        if 90.0 <= colong < 270.0:
            return TimeOfDay.EVENING.name
        else:
            return TimeOfDay.MORNING.name

    def time_from_new_moon(self) -> float:
        """Time (hours) from the previous new moon.

        This function calculates the time from the previous new moon.

        Returns
        -------
        float
            The time from new moon.
        """
        previous_new_moon = ephem.previous_new_moon(self.observer.date)
        return float(MoonInfo.DAYS_TO_HOURS * (self.observer.date - previous_new_moon))

    def time_to_full_moon(self) -> float:
        """Time (days) to the next full moon.

        This function calculates the time to the next full moon.

        Returns
        -------
        float
            The time to full moon.
        """
        next_full_moon = ephem.next_full_moon(self.observer.date)
        return float(next_full_moon - self.observer.date)

    def time_to_new_moon(self) -> float:
        """Time (hours) to the next new moon.

        This function calculates the time to the next new moon.

        Returns
        -------
        float
            The time to new moon.
        """
        next_new_moon = ephem.next_new_moon(self.observer.date)
        return float(MoonInfo.DAYS_TO_HOURS * (next_new_moon - self.observer.date))

    def update(self, datetime: DateTimeTuple) -> None:
        """Update the moon information based on time.

        This fuction updates the Observer instance's datetime setting. The
        incoming datetime tuple should be in UTC with the following placement
        of values: (YYYY, m, d, H, M, S) as defined below::

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
