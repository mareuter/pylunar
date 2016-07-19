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
    14.613899383497483
    >>> mi.fractional_phase()
    0.9900636126401263
