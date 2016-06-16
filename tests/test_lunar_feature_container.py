from pylunar import LunarFeatureContainer


class TestLunarFeatureContainer(object):

    def test_basic_information_after_creation(self):
        lfc = LunarFeatureContainer()

        assert len(lfc) == 0

    def test_short_load(self):
        lfc = LunarFeatureContainer()
        lfc.load(limit=10)

        assert len(lfc) == 10
        assert len(lfc.club_type) == 2
        assert len(lfc.feature_type) == 4

    def test_iterator(self):
        lfc = LunarFeatureContainer()
        lfc.load(limit=2)

        assert len(lfc) == 2
        ilfc = iter(lfc)
        feature = next(ilfc)

        assert feature.name == "Montes Jura"
