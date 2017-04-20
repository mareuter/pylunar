from pylunar import MoonInfo


class TestMoonInfo(object):

    def setup_class(self):
        location = ((35, 58, 10), (-84, 19, 0))
        self.obs_datetime = (2013, 10, 18, 22, 0, 0)
        self.mi = MoonInfo(location[0], location[1])

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

        next_four_phases = self.mi.next_four_phases()
        phase_names = [x[0] for x in next_four_phases]
        assert phase_names == ["full_moon", "last_quarter", "new_moon", "first_quarter"]
        assert next_four_phases[0][1] == (2013, 10, 18, 23, 37, 39.644067962653935)

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
