# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2016, Michael Reuter
# Distributed under the MIT License. See LICENSE for more information.
# ------------------------------------------------------------------------------
import ephem

from pylunar import tuple_to_string

__all__ = ["MoonInfo"]


class MoonInfo(object):
    """Handle all moon information.

    Attributes
    ----------
    observer : ephem.Observer instance.
        The instance containing the observer's location information.
    """

    def __init__(self, latitude, longitude, name=None):
        """Initialize the class.

        Parameters
        ----------
        latitude : tuple of 3 ints
            The latitude of the observer.
        longitude : tuple of 3 ints
            The longitude of the observer.
        name : str, optional
            A name for the observer's location.
        """
        self.observer = ephem.Observer()
        self.observer.lat = tuple_to_string(latitude)
        self.observer.long = tuple_to_string(longitude)
        self.moon = ephem.Moon()
