from pylunar import tuple_to_string


class TestHelperFunctions(object):

    def test_tuple_to_string(self):
        coordinate = (-34, 23, 12)
        assert tuple_to_string(coordinate) == "-34:23:12"
