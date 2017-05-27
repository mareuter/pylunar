# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2016, Michael Reuter
# Distributed under the MIT License. See LICENSE for more information.
# ------------------------------------------------------------------------------
"""Module for helper functions.
"""

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
        values = [round(x) for x in ephem.Date(mjd).tuple()]
        if values[-1] == 60:
            values[-1] = 0
        return tuple(values)
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
