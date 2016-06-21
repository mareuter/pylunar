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
