from pylunar import mjd_to_date_tuple, tuple_to_string


class TestHelperFunctions(object):

    def test_tuple_to_string(self):
        coordinate = (-34, 23, 12)
        assert tuple_to_string(coordinate) == "-34:23:12"

    def test_mjd_to_date_tuple(self):
        date_tuple = mjd_to_date_tuple(41564.48448662116)
        assert date_tuple == (2013, 10, 18, 23, 37, 39.644067962653935)
