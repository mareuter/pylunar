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

__all__ = ["mjd_to_date_tuple", "tuple_to_string"]

import ephem


def mjd_to_date_tuple(mjd, round_off=False):
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
    if round_off:
        return tuple(int(x) for x in ephem.Date(mjd).tuple())
    else:
        return ephem.Date(mjd).tuple()


def tuple_to_string(coord):
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
