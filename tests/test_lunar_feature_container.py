from pylunar import LunarFeatureContainer


class TestLunarFeatureContainer(object):

    def setup_class(self):
        self.lfc = LunarFeatureContainer()

    def test_basic_information_after_creation(self):
        assert len(self.lfc) == 0

    def test_short_load(self):
        self.lfc.load(limit=10)

        assert len(self.lfc) == 10
        assert len(self.lfc.club_type) == 2
        assert len(self.lfc.feature_type) == 4

    def test_iterator(self):
        self.lfc.load(limit=2)

        assert len(self.lfc) == 2
        ilfc = iter(self.lfc)
        feature = next(ilfc)

        assert feature.name == "Montes Jura"
