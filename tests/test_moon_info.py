from pylunar import MoonInfo


class TestMoonInfo(object):

    def test_basic_information_after_creation(self):
        location = (((35, 58, 10)), (-84, 19, 0))
        mi = MoonInfo(location[0], location[1])

        assert mi.observer is not None
        assert mi.moon is not None
