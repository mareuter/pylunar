# This file is part of pylunar.
#
# Developed by Michael Reuter.
#
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Module for helper functions."""

from __future__ import annotations

__all__ = ["mjd_to_date_tuple", "tuple_to_string"]

import ephem

from .pkg_types import DateTimeTuple, DmsCoordinate


def mjd_to_date_tuple(mjd: float, round_off: bool = False) -> DateTimeTuple:
    """Convert a Modified Julian date to a UTC time tuple.

    Parameters
    ----------
    mjd : float
        The Modified Julian Date to convert.
    round_off : bool, optional
        Flag to round the seconds.

    Returns
    -------
    tuple
        The UTC time for the MJD.
    """
    date_tuple: DateTimeTuple
    date_tuple = tuple(int(x) for x in ephem.Date(mjd).tuple()) if round_off else ephem.Date(mjd).tuple()
    return date_tuple


def tuple_to_string(coord: DmsCoordinate) -> str:
    """Return a colon-delimited string.

    Parameters
    ----------
    coord : tuple of 3 ints
        The coordinate to transform.

    Returns
    -------
    str
        The colon-delimited coordinate string.
    """
    return ":".join([str(x) for x in coord])
