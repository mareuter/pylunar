from pylunar import LunarFeature, MoonInfo


class TestMoonInfo(object):

    def setup_class(self):
        location = ((35, 58, 10), (-84, 19, 0))
        self.obs_datetime = (2013, 10, 18, 22, 0, 0)
        self.timezone = 'America/New_York'
        self.mi = MoonInfo(location[0], location[1])
        self.date_list = [(2013, 10, 5, 0, 0, 0),
                          (2013, 10, 8, 6, 0, 0),
                          (2013, 10, 11, 22, 0, 0),
                          (2013, 10, 12, 3, 30, 0),
                          (2013, 10, 19, 1, 30, 0),
                          (2013, 10, 24, 15, 0, 0),
                          (2013, 10, 26, 23, 40, 0),
                          (2013, 11, 2, 23, 0, 0)]

    def test_basic_information_after_creation(self):
        assert self.mi.observer is not None
        assert self.mi.moon is not None

    def test_information_after_update(self):
        self.mi.update(self.obs_datetime)
        assert self.mi.observer.date == 41564.416666666664

    def test_moon_information(self):
        self.mi.update(self.obs_datetime)

        assert self.mi.age() == 13.892695861570246
        assert self.mi.colong() == 83.97189956624061
        assert self.mi.fractional_phase() == 0.9998519924481626
        assert self.mi.phase_name() == "FULL_MOON"
        assert self.mi.libration_lon() == 5.23107551788429
        assert self.mi.libration_lat() == -1.4788210646482465
        assert self.mi.altitude() == -9.8149186580585
        assert self.mi.azimuth() == 69.75156520051686
        assert self.mi.time_from_new_moon() == 333.4247006776859
        assert self.mi.time_to_new_moon() == 374.8327396878158
        assert self.mi.time_to_full_moon() == 0.06781995449273381
        assert self.mi.ra() == 23.331888825304354
        assert self.mi.dec() == 10.129795148334347
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
        assert next_four_phases[0][1] == (2013, 10, 18, 23, 37, 39.644067962653935)

    def test_different_elongations(self):
        self.mi.update((2013, 10, 6, 22, 0, 0))
        assert self.mi.elongation() == 23.90241813659668
        self.mi.update((2013, 10, 24, 22, 0, 0))
        assert self.mi.elongation() == 247.54827117919922
        self.mi.update((2013, 10, 31, 22, 0, 0))
        assert self.mi.elongation() == 326.54500579833984

    def test_different_rise_set_times(self):
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

    def test_state_reset_after_rise_test_call(self):
        self.mi.update(self.obs_datetime)
        self.mi.rise_set_times(self.timezone)
        assert self.mi.colong() == 83.97189956624061

    def test_different_phase_names(self):
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

    def test_colong_to_long(self):
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

    def test_time_of_day(self):
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

    def test_is_visible(self):
        feature1 = LunarFeature("A", 0.1, 0.0, 46.0, 0.01, 0.01, "Crater",
                                "Taruntius", "LAC-61", "Lunar", "Telescope")
        feature2 = LunarFeature("B", 1.0, 50.0, 46.0, 0.5, 0.5, "Crater",
                                "Endymion", "LAC-14", "Lunar", "Binocular")
        feature3 = LunarFeature("C", 100.0, -30.0, 46.0, 5.0, 10.0, "Mare",
                                "Fracastorius", "LAC-97", "Lunar", "Naked Eye")
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
