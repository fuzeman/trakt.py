Contribution Guide
------------------

- `Reporting Bugs`_
- `Requesting features`_
- `Suggesting enhancements`_
- `Pull Requests`_

Reporting Bugs
--------------

Please explain the bug and include any details which might help reproduce the issue, for example:

- Reproduction steps or example script *(if possible)*
- Platform details *(e.g. Operating System, CPU Type, Device Model)*
- Python version:

  .. code-block:: shell

    python -V

- Installed packages:

  .. code-block:: shell

    pip freeze

Requesting features
-------------------

Please detail the feature you would like to see in the library and include any relevant information, for example:

- Link to the relevant method in the `Trakt.tv API Specification`_

Suggesting enhancements
-----------------------

Please detail your suggested enhancement and include any relevant information, for example:

- Link to the relevant method in the `Trakt.tv API Specification`_
- Current library functionality (on the latest official release)
- Would this enhancement break compatibility? could this be resolved in any way (e.g. method proxies)?

Pull Requests
-------------

**Please ensure:**

- Your changes are based on the *develop* branch, before starting development checkout the correct branch:

  .. code-block:: shell

    git checkout develop

- Tests pass, either:

  - Use `tox`_ to run tests against each version of Python and PyPy:

    .. code-block:: shell

      tox

  - Test against your current version of Python:

    .. code-block:: shell

      python setup.py test

  - Create your pull request, and wait for the test results to be posted by Travis CI. *(this may take a few minutes)*

- No issues are reported by `flake8`_, either:

  - Use `tox`_ to run `flake8`_:

    .. code-block:: shell

      tox flake8

  - Create your pull request, and wait for the test results to be posted by Travis CI. *(this may take a few minutes)*

    **Note:** `flake8`_ results will be displayed under the "Python 3.6" job.

- Test coverage hasn't fallen *(lines added without tests)*

  - Use `tox`_ to run tests against each version of Python and PyPy:

    .. code-block:: shell

      tox

    *Coverage details will be displayed in the "stats" task.*

  - Create your pull request, and wait for the coverage details to be posted by Coveralls. *(this may take a few minutes)*

If you aren't sure how to write tests or are confused about any of the above steps, just post the pull request anyway. I'll either let you
know what needs to be changed, or can just cleanup your code and write the required tests (if requested).

.. _flake8: http://flake8.pycqa.org
.. _Trakt.tv API Specification: http://docs.trakt.apiary.io
.. _tox: https://tox.readthedocs.io
