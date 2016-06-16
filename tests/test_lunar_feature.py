from pylunar import LunarFeature


class TestLunarFeature(object):

    def test_basic_information_after_creation(self):
        feature_info = ("Clavius", -58.622830884248, -14.727490317559,
                        "Crater", 7.61545753479, 14.614604949952,
                        "Both", "Binocular")
        lf = LunarFeature(*feature_info)
        assert lf.name == "Clavius"
        assert lf.latitude == -58.622830884248
        assert lf.lunar_club_type == "Binocular"

        val = str(lf)
        assert val.startswith("Name")

    def test_creation_from_database_row(self):
        feature_row = (33, "Clavius", 230.77, -58.622830884248, -14.727490317559, 7.61545753479,
                       14.614604949952, "Crater", "Clavius", "LAC-126", "Both", "Binocular")
        lf = LunarFeature.from_row(feature_row)
        assert lf.name == "Clavius"
        assert lf.latitude == -58.622830884248
        assert lf.lunar_club_type == "Binocular"
