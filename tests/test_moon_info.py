# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Tests for the MoonInfo class."""

from pylunar import LunarFeature, MoonInfo


class TestMoonInfo:
    def setup_class(self) -> None:
        location = ((35, 58, 10), (-84, 19, 0))
        self.obs_datetime = (2013, 10, 18, 22, 0, 0)
        self.timezone = "America/New_York"
        self.mi = MoonInfo(location[0], location[1])
        self.date_list = [
            (2013, 10, 5, 0, 0, 0),
            (2013, 10, 8, 6, 0, 0),
            (2013, 10, 11, 22, 0, 0),
            (2013, 10, 12, 3, 30, 0),
            (2013, 10, 19, 1, 30, 0),
            (2013, 10, 24, 15, 0, 0),
            (2013, 10, 26, 23, 40, 0),
            (2013, 11, 2, 23, 0, 0),
        ]

    def test_basic_information_after_creation(self) -> None:
        assert self.mi.observer is not None
        assert self.mi.moon is not None

    def test_information_after_update(self) -> None:
        self.mi.update(self.obs_datetime)
        assert self.mi.observer.date == 41564.416666666664

    def test_moon_information(self) -> None:
        self.mi.update(self.obs_datetime)

        assert self.mi.age() == 13.892695999260468
        assert self.mi.fractional_age() == 0.4707676682458111
        assert self.mi.colong() == 83.97189956624061
        assert self.mi.fractional_phase() == 0.9998519924481626
        assert self.mi.phase_name() == "FULL_MOON"
        assert self.mi.libration_lon() == 5.23107551788429
        assert self.mi.libration_lat() == -1.4788210646482465
        assert self.mi.libration_phase_angle() == 105.7855572234932
        assert self.mi.altitude() == -9.814919511832146
        assert self.mi.azimuth() == 69.75156520051686
        assert self.mi.time_from_new_moon() == 333.42470398225123
        assert self.mi.time_to_new_moon() == 374.83273694326635
        assert self.mi.time_to_full_moon() == 0.0678198272944428
        assert self.mi.ra() == 23.331890450649784
        assert self.mi.dec() == 10.129795616523591
        assert self.mi.earth_distance() == 386484.25078267464
        assert self.mi.angular_size() == 0.5159071519639757
        assert self.mi.magnitude() == -12.63
        assert self.mi.subsolar_lat() == -0.3366501792590513
        assert self.mi.elongation() == 178.56298828125

        rise_set_times = self.mi.rise_set_times(self.timezone)
        position_names = [x[0] for x in rise_set_times]
        assert position_names == ["transit", "set", "rise"]
        assert rise_set_times[0][1] == (2013, 10, 18, 0, 43, 21)

        next_four_phases = self.mi.next_four_phases()
        phase_names = [x[0] for x in next_four_phases]
        assert phase_names == ["full_moon", "last_quarter", "new_moon", "first_quarter"]
        assert next_four_phases[0][1] == (2013, 10, 18, 23, 37, 39.633078)

    def test_different_elongations(self) -> None:
        self.mi.update((2013, 10, 6, 22, 0, 0))
        assert self.mi.elongation() == 23.902420043945312
        self.mi.update((2013, 10, 24, 22, 0, 0))
        assert self.mi.elongation() == 247.54827117919922
        self.mi.update((2013, 10, 31, 22, 0, 0))
        assert self.mi.elongation() == 326.54500579833984

    def test_different_rise_set_times(self) -> None:
        self.mi.update((2013, 10, 17, 22, 0, 0))
        rise_set_times = self.mi.rise_set_times(self.timezone)
        position_names = [x[0] for x in rise_set_times]
        assert position_names == ["transit", "set", "rise"]
        assert rise_set_times[0][1] == "Does not transit"
        self.mi.update((2013, 9, 26, 22, 0, 0))
        rise_set_times = self.mi.rise_set_times(self.timezone)
        position_names = [x[0] for x in rise_set_times]
        assert position_names == ["rise", "transit", "set"]
        assert rise_set_times[0][1] == "Does not rise"

    def test_state_reset_after_rise_test_call(self) -> None:
        self.mi.update(self.obs_datetime)
        self.mi.rise_set_times(self.timezone)
        assert self.mi.colong() == 83.97189956624061

    def test_different_phase_names(self) -> None:
        self.mi.update((2013, 10, 18, 18, 0, 0))
        assert self.mi.phase_name() == "WAXING_GIBBOUS"
        self.mi.update((2013, 10, 5, 0, 0, 0))
        assert self.mi.phase_name() == "NEW_MOON"
        self.mi.update((2013, 10, 8, 6, 0, 0))
        assert self.mi.phase_name() == "WAXING_CRESCENT"
        self.mi.update((2013, 10, 11, 22, 0, 0))
        assert self.mi.phase_name() == "FIRST_QUARTER"
        self.mi.update((2013, 10, 12, 3, 30, 0))
        assert self.mi.phase_name() == "WAXING_GIBBOUS"
        self.mi.update((2013, 10, 19, 1, 30, 0))
        assert self.mi.phase_name() == "FULL_MOON"
        self.mi.update((2013, 10, 24, 15, 0, 0))
        assert self.mi.phase_name() == "WANING_GIBBOUS"
        self.mi.update((2013, 10, 26, 23, 40, 0))
        assert self.mi.phase_name() == "LAST_QUARTER"
        self.mi.update((2013, 11, 2, 23, 0, 0))
        assert self.mi.phase_name() == "WANING_CRESCENT"

    def test_different_phase_emoji(self) -> None:
        self.mi.update((2013, 10, 18, 18, 0, 0))
        assert self.mi.phase_emoji() == "🌔"
        self.mi.update((2013, 10, 5, 0, 0, 0))
        assert self.mi.phase_emoji() == "🌑"
        self.mi.update((2013, 10, 8, 6, 0, 0))
        assert self.mi.phase_emoji() == "🌒"
        self.mi.update((2013, 10, 11, 22, 0, 0))
        assert self.mi.phase_emoji() == "🌓"
        self.mi.update((2013, 10, 12, 3, 30, 0))
        assert self.mi.phase_emoji() == "🌔"
        self.mi.update((2013, 10, 19, 1, 30, 0))
        assert self.mi.phase_emoji() == "🌕"
        self.mi.update((2013, 10, 24, 15, 0, 0))
        assert self.mi.phase_emoji() == "🌖"
        self.mi.update((2013, 10, 26, 23, 40, 0))
        assert self.mi.phase_emoji() == "🌗"
        self.mi.update((2013, 11, 2, 23, 0, 0))
        assert self.mi.phase_emoji() == "🌘"

    def test_colong_to_long(self) -> None:
        self.mi.update(self.date_list[0])
        assert self.mi.colong_to_long() == 85.63604081994191
        self.mi.update(self.date_list[1])
        assert self.mi.colong_to_long() == 46.01878527028475
        self.mi.update(self.date_list[2])
        assert self.mi.colong_to_long() == 1.2909929717534965
        self.mi.update(self.date_list[3])
        assert self.mi.colong_to_long() == -1.5152263359641438
        self.mi.update(self.date_list[4])
        assert self.mi.colong_to_long() == -85.74623915427537
        self.mi.update(self.date_list[5])
        assert self.mi.colong_to_long() == 26.4615811331646
        self.mi.update(self.date_list[6])
        assert self.mi.colong_to_long() == -2.1812638653489103
        self.mi.update(self.date_list[7])
        assert self.mi.colong_to_long() == -87.15293941124628

    def test_time_of_day(self) -> None:
        self.mi.update(self.date_list[0])
        assert self.mi.time_of_day() == "MORNING"
        self.mi.update(self.date_list[1])
        assert self.mi.time_of_day() == "MORNING"
        self.mi.update(self.date_list[2])
        assert self.mi.time_of_day() == "MORNING"
        self.mi.update(self.date_list[3])
        assert self.mi.time_of_day() == "MORNING"
        self.mi.update(self.date_list[4])
        assert self.mi.time_of_day() == "MORNING"
        self.mi.update(self.date_list[5])
        assert self.mi.time_of_day() == "EVENING"
        self.mi.update(self.date_list[6])
        assert self.mi.time_of_day() == "EVENING"
        self.mi.update(self.date_list[7])
        assert self.mi.time_of_day() == "EVENING"

    def test_is_visible(self) -> None:
        feature1 = LunarFeature(
            "A", 0.1, 0.0, 46.0, 0.01, 0.01, "Crater", "Taruntius", "LAC-61", "Lunar", "Telescope"
        )
        feature2 = LunarFeature(
            "B", 1.0, 50.0, 46.0, 0.5, 0.5, "Crater", "Endymion", "LAC-14", "Lunar", "Binocular"
        )
        feature3 = LunarFeature(
            "C", 100.0, -30.0, 46.0, 5.0, 10.0, "Mare", "Fracastorius", "LAC-97", "Lunar", "Naked Eye"
        )
        self.mi.update(self.date_list[0])
        assert self.mi.is_visible(feature1) is False
        assert self.mi.is_visible(feature2) is False
        assert self.mi.is_visible(feature3) is False
        self.mi.update((2013, 10, 8, 6, 15, 0))
        assert self.mi.is_visible(feature1) is True
        assert self.mi.is_visible(feature2) is False
        assert self.mi.is_visible(feature3) is False
        self.mi.update((2013, 10, 8, 7, 0, 0))
        assert self.mi.is_visible(feature1) is True
        assert self.mi.is_visible(feature2) is True
        assert self.mi.is_visible(feature3) is False
        self.mi.update((2013, 10, 8, 16, 0, 0))
        assert self.mi.is_visible(feature1) is True
        assert self.mi.is_visible(feature2) is True
        assert self.mi.is_visible(feature3) is True
        self.mi.update((2013, 10, 9, 12, 0, 0))
        assert self.mi.is_visible(feature1) is False
        assert self.mi.is_visible(feature2) is True
        assert self.mi.is_visible(feature3) is True
        self.mi.update((2013, 10, 10, 5, 0, 0))
        assert self.mi.is_visible(feature1) is False
        assert self.mi.is_visible(feature2) is False
        assert self.mi.is_visible(feature3) is True
        self.mi.update((2013, 10, 21, 2, 30, 0))
        assert self.mi.is_visible(feature1) is False
        assert self.mi.is_visible(feature2) is True
        assert self.mi.is_visible(feature3) is True
        self.mi.update((2013, 10, 21, 19, 0, 0))
        assert self.mi.is_visible(feature1) is True
        assert self.mi.is_visible(feature2) is True
        assert self.mi.is_visible(feature3) is True
        self.mi.update((2013, 10, 22, 15, 0, 0))
        assert self.mi.is_visible(feature1) is True
        assert self.mi.is_visible(feature2) is True
        assert self.mi.is_visible(feature3) is False
        self.mi.update((2013, 10, 23, 0, 0, 0))
        assert self.mi.is_visible(feature1) is True
        assert self.mi.is_visible(feature2) is False
        assert self.mi.is_visible(feature3) is False
        self.mi.update((2013, 10, 23, 1, 0, 0))
        assert self.mi.is_visible(feature1) is False
        assert self.mi.is_visible(feature2) is False
        assert self.mi.is_visible(feature3) is False

    def test_is_libration_ok(self) -> None:
        feature1 = LunarFeature(
            "A", 374.0, -2.0, 87.0, 12.0, 12.0, "Mare", "Ansgarius", "LAC-81", "LunarII", None
        )
        feature2 = LunarFeature("B", 358.0, 13.0, 86.5, 9.0, 12.0, "Mare", "Neper", "LAC-63", "LunarII", None)
        feature3 = LunarFeature(
            "C", 682.0, -19.5, -95.0, 22.5, 23.0, "Mons", "Mare Orientale", "LAC-108", "LunarII", None
        )
        self.mi.update((2017, 5, 27, 12, 21, 0))
        assert self.mi.is_libration_ok(feature1) is True
        assert self.mi.is_libration_ok(feature2) is True
        assert self.mi.is_libration_ok(feature3) is False
        assert self.mi.is_visible(feature1) is True
        self.mi.update((2017, 11, 24, 22, 0, 0))
        assert self.mi.is_libration_ok(feature1) is False
        assert self.mi.is_libration_ok(feature2) is False
        assert self.mi.is_visible(feature2) is False
        assert self.mi.is_libration_ok(feature3) is True
        assert self.mi.is_visible(feature3) is False
        self.mi.update((2017, 7, 17, 6, 0, 0))
        assert self.mi.is_libration_ok(feature1) is False
        assert self.mi.is_libration_ok(feature2) is False
        assert self.mi.is_libration_ok(feature3) is True
