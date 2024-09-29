.. :changelog:

History
-------

0.7.3 (2024-09-29)
++++++++++++++++++

* Updates to project dependencies

0.7.2 (2024-02-26)
++++++++++++++++++

* Change types module to pkg_types to avoid shadowing builtin

0.7.1 (2024-02-11)
++++++++++++++++++

* Drop support for Python 3.6 and 3.7
* Add Python 3.9, 3.10, 3.11 and 3.12 support
* Switch to pyproject.toml
* Internal package updates
* Update docs infrastructure
* Switch back to tox
* Add linting and formatting
* Add mypy and typing
* Add numpydoc and tox.ini checking

0.7.0 (2023-12-31)
++++++++++++++++++

* Add phase emoji function
* Add phase ASCII art function
* Add fractional age function
* Updates to API docs
* Infrastructure updates and fixes

0.6.0 (2020-04-07)
++++++++++++++++++

* Drop Python 2 and 3.4 and 3.5 support
* Add Python 3.7 and 3.8 support
* Change to 3-clause BSD license
* Switch to pytest from tox
* Add Github workflows for build and package upload
* Remove Travis

0.5.1 (2018-04-20)
++++++++++++++++++

* Add changelog updates

0.5.0 (2018-04-20)
++++++++++++++++++

* LunarFeature additions

  * Latitude and Longitude ranges
  * Feature angle
* MoonInfo additions

  * Libration phase angle
  * Libration visibility check
  * Updated is_visible to use libration visibility check

0.4.1 (2017-05-30)
++++++++++++++++++

* Corrected moon state after rise/set function call
* Made landing sites always visible once visible

0.4.0 (2017-05-28)
++++++++++++++++++

* Added landing sites to feature database
* Expanding LunarFeature content
* MoonInfo object additions

  * right ascension and declination
  * solar elongation
  * earth distance
  * rise, transit and set times
  * angular size
  * magnitude
  * sub-solar latitude

0.3.1 (2017-05-15)
++++++++++++++++++

* Ensure feature DB included in package

0.3.0 (2017-05-15)
++++++++++++++++++

* MoonInfo object additions

  * time of day
  * is feature visible

* LunarFeatureContainer object changes

  * Made constructor club related
  * Load call can check if feature is visible using MoonInfo instance

0.2.1 (2017-04-20)
++++++++++++++++++

* Changed mechanism to determine phase name

0.2.0 (2017-04-16)
++++++++++++++++++

* MoonInfo object additions

  * phase name
  * time from new moon
  * time to new moon
  * time to full moon

0.1.0 (2016-07-18)
++++++++++++++++++

* MoonInfo object that provides basic lunar information

  * age
  * altitude
  * azimuth
  * colongitude
  * fractional phase
  * libration latitude
  * libration longitude
  * next four lunar phases

