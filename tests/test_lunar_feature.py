# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Tests for the LunarFeature class."""

from pylunar import LunarFeature


class TestLunarFeature:
    def setup_class(self) -> None:
        self.feature_info = (
            "Clavius",
            230.77,
            -58.622830884248,
            -14.727490317559,
            7.61545753479,
            14.614604949952,
            "Crater",
            "Clavius",
            "LAC-126",
            "Both",
            "Binocular",
        )

    def test_basic_information_after_creation(self) -> None:
        lf = LunarFeature(*self.feature_info)
        assert lf.name == self.feature_info[0]
        assert lf.diameter == self.feature_info[1]
        assert lf.latitude == self.feature_info[2]
        assert lf.longitude == self.feature_info[3]
        assert lf.delta_latitude == self.feature_info[4]
        assert lf.delta_longitude == self.feature_info[5]
        assert lf.feature_type == self.feature_info[6]
        assert lf.quad_name == self.feature_info[7]
        assert lf.quad_code == self.feature_info[8]
        assert lf.code_name == self.feature_info[9]
        assert lf.lunar_club_type == self.feature_info[10]
        assert lf.latitude_range() == (-62.430559651643, -54.815102116853005)
        assert lf.longitude_range() == (-22.034792792535, -7.420187842583001)
        assert lf.feature_angle() == 194.10225514559056

        val = str(lf)
        assert val.startswith("Name")

    def test_creation_from_database_row(self) -> None:
        feature_row = (
            33,
            "Clavius",
            230.77,
            -58.622830884248,
            -14.727490317559,
            7.61545753479,
            14.614604949952,
            "Crater",
            "Clavius",
            "LAC-126",
            "Both",
            "Binocular",
        )
        lf = LunarFeature.from_row(feature_row)
        assert lf.name == feature_row[1]
        assert lf.diameter == feature_row[2]
        assert lf.latitude == feature_row[3]
        assert lf.longitude == feature_row[4]
        assert lf.delta_latitude == feature_row[5]
        assert lf.delta_longitude == feature_row[6]
        assert lf.feature_type == feature_row[7]
        assert lf.quad_name == feature_row[8]
        assert lf.quad_code == feature_row[9]
        assert lf.code_name == feature_row[10]
        assert lf.lunar_club_type == feature_row[11]

    def test_list_from_feature(self) -> None:
        lf = LunarFeature(*self.feature_info)
        feature_list = lf.list_from_feature()
        for value, truth in zip(feature_list, self.feature_info):
            assert value == truth
