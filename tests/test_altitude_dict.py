# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Tests for AltitudeDict class."""

from pylunar import AltitudeDict, MoonInfo


class TestAltitudeDict:
    def setup_class(self) -> None:
        self.ad = AltitudeDict()

    def test_basic_information_after_creation(self) -> None:
        assert len(self.ad) == 0

    def test_information_after_load(self) -> None:
        location = ((35, 58, 10), (-84, 19, 0))
        mi = MoonInfo(location[0], location[1])
        mi.update((2013, 10, 12, 18, 0, 0))

        self.ad.load(mi)
        assert len(self.ad) == 4
        assert list(self.ad.keys()) == ["Byrgius A", "Proclus", "Rupes Recta", "Tycho"]
        assert self.ad["Rupes Recta"] == 1.3038753306292297
