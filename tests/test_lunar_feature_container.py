# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Tests for the LunarFeatureContainer class."""

from pylunar import LunarFeatureContainer, MoonInfo


class TestLunarFeatureContainer:
    def setup_class(self) -> None:
        self.lc_lfc = LunarFeatureContainer("Lunar")
        self.lc2_lfc = LunarFeatureContainer("LunarII")

    def test_basic_information_after_creation(self) -> None:
        assert len(self.lc_lfc) == 0
        assert len(self.lc2_lfc) == 0

    def test_short_load(self) -> None:
        self.lc_lfc.load(limit=10)
        assert len(self.lc_lfc) == 10
        assert len(self.lc_lfc.club_type) == 2
        assert len(self.lc_lfc.feature_type) == 4

        self.lc2_lfc.load(limit=10)
        assert len(self.lc2_lfc) == 10
        assert len(self.lc2_lfc.club_type) == 2
        assert len(self.lc2_lfc.feature_type) == 5

    def test_iterator(self) -> None:
        self.lc_lfc.load(limit=2)
        assert len(self.lc_lfc) == 2
        ilfc = iter(self.lc_lfc)
        feature = next(ilfc)
        assert feature.name == "Vallis Alpes"

        self.lc2_lfc.load(limit=2)
        assert len(self.lc2_lfc) == 2
        ilfc2 = iter(self.lc2_lfc)
        feature2 = next(ilfc2)
        assert feature2.name == "Montes Jura"

    def test_visibility(self) -> None:
        location = ((35, 58, 10), (-84, 19, 0))
        mi = MoonInfo(location[0], location[1])
        mi.update((2013, 10, 12, 18, 0, 0))

        # Need to create new containers.
        lc_lfc = LunarFeatureContainer("Lunar")
        lc2_lfc = LunarFeatureContainer("LunarII")

        lc_lfc.load(mi, limit=10)
        assert len(lc_lfc) == 6
        assert len(lc_lfc.club_type) == 2
        assert len(lc_lfc.feature_type) == 4
        ilfc = iter(lc_lfc)
        feature = next(ilfc)
        assert feature.name == "Vallis Alpes"

        lc2_lfc.load(mi, limit=10)
        assert len(lc2_lfc) == 2
        assert len(lc2_lfc.club_type) == 2
        assert len(lc2_lfc.feature_type) == 2
        ilfc2 = iter(lc2_lfc)
        feature2 = next(ilfc2)
        assert feature2.name == "Vallis Alpes"
