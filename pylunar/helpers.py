# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2016, Michael Reuter
# Distributed under the MIT License. See LICENSE for more information.
# ------------------------------------------------------------------------------
"""Module for helper functions.
"""


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
