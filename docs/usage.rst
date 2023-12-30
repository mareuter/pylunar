========
Usage
========

To use Python Lunar in a project::

	>>> import pylunar

Location: Boston, MA, USA

    >>> mi = pylunar.MoonInfo((42, 21, 30), (-71, 3, 35))

Local Time: July 18, 2016 at 21:45

API requires UTC, so add 4 hours since on Daylight Savings (changes day)

    >>> mi.update((2016, 7, 19, 1, 45, 0))
    >>> mi.age()
    14.613897646951955
    >>> mi.fractional_phase()
    0.9900636126401263
    >>> mi.phase_name()
    'WAXING_GIBBOUS'

This package also contains the :py:class:`.LunarFeatureContainer` class which holds features on the moon for the Astronomical League's Lunar Club and Lunar II observing programs. To create a container for the Lunar Club program, do.

	>>> lc = pylunar.LunarFeatureContainer("Lunar")
	>>> lc.load()
	>>> len(lc)
	90

There are 90 features available to this observing program. The container allows one to filter those features based on the position of the lunar terminator with respect to a given feature. The :py:meth:`.LunarFeatureContainer.load` method can be passed a :py:class:`.MoonInfo` instance to perform that filtering.

	>>> lc.load(mi)
	>>> len(lc)
	12

A container for Lunar II can be created by passing the `LunarII` string to the constructor of :py:class:`.LunarFeatureContainer`.

Feature instances (:py:class:`.LunarFeature`) can be obtained from the container in usual manner.

	>>> for feature in lc:
	...     print(feature)
	Name = Grimaldi
	Lat/Long = (-5.38, -68.36)
	Type = Crater
	Delta Lat/Long = (5.72, 5.74)
	Name = Mare Crisium
	Lat/Long = (16.18, 59.10)
	Type = Mare
	Delta Lat/Long = (14.85, 19.02)
	...
