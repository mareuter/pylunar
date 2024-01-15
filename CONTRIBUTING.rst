============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/mareuter/pylunar/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Python Lunar could always use more documentation, whether as part of the
official Python Lunar docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/mareuter/pylunar/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `pylunar` for
local development.

#. Fork the `pylunar` repo on GitHub.
#. Create a vitrual environment for dependency installation.
#. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pylunar.git

#. Install the dependencies for development and pre-commit hook::

    $ make init

#. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

#. When you're done making changes, check that your changes pass style and unit
   tests::

    $ tox

#. Commit your changes (this will cause the pre-commit hook to run) and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

#. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

#. The pull request should include tests.
#. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in HISTORY.rst.
#. The pull request should work for the supported range of Python versions.
   The pull request will run GitHub actions to perform those checks.
   Check https://github.com/mareuter/pylunar/pulls
   for active pull requests and make sure that the checks all passed.


Tips
----

To run a subset of tests::

	 $ pytest test/test_pylunar.py
