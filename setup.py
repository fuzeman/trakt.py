#!/usr/bin/env python

"""trakt.py setup script (powered by pbr)."""

from setuptools import setup
import sys

NEEDS_PYTEST = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
PYTEST_RUNNER = ['pytest-runner>=2.0.0'] if NEEDS_PYTEST else []


setup(
    setup_requires=PYTEST_RUNNER + [
        'pbr>=1.9',
        'setuptools>=17.1'
    ],
    pbr=True,
)
