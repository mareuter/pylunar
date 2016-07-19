# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2016, Michael Reuter
# Distributed under the MIT License. See LICENSE for more information.
# ------------------------------------------------------------------------------
"""Module for helper functions.
"""

import ephem


def mjd_to_date_tuple(mjd):
    """Convert a Modified Julian date to a UTC time tuple.

    Parameters
    ----------
    mjd : float
        The Modified Julian Date to convert.

    Returns
    -------
    tuple
        The UTC time for the MJD.
    """
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
