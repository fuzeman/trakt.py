#!/usr/bin/env python

"""trakt.py setup script (powered by pbr)."""

from __future__ import absolute_import, division, print_function

from setuptools import setup
import sys

NEEDS_PYTEST = set(['pytest', 'test', 'ptr']).intersection(sys.argv)
PYTEST_RUNNER = ['pytest-runner>=2.0.0'] if NEEDS_PYTEST else []


setup(
    setup_requires=PYTEST_RUNNER + [
        'pbr>=1.9,<=3.1.1',
        'setuptools>=17.1'
    ],
    pbr=True,
)
