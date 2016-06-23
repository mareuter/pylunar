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
        assert self.mi.libration_lon() == 5.23107551788429
        assert self.mi.libration_lat() == -1.4788210646482465
        assert self.mi.altitude() == -9.8149186580585
        assert self.mi.azimuth() == 69.75156520051686

        next_four_phases = self.mi.next_four_phases()
        phase_names = [x[0] for x in next_four_phases]
        assert phase_names == ["full", "tq", "new", "fq"]
        assert next_four_phases[0][1] == (2013, 10, 18, 23, 37, 39.644067962653935)
