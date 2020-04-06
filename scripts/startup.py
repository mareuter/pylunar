# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

from pylunar import MoonInfo
location = ((35, 58, 10), (-84, 19, 0))
obs_datetime = (2013, 10, 18, 22, 0, 0)
mi = MoonInfo(location[0], location[1])
mi.update(obs_datetime)
