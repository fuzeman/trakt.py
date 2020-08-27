from __future__ import absolute_import, division, print_function

from trakt.core.helpers import from_iso8601_datetime, to_iso8601_datetime

from hamcrest import assert_that, equal_to
import pytest

try:
    import arrow
except ImportError:
    arrow = None


def test_datetime_conversion():
    if arrow is None:
        pytest.skip('arrow not installed, skipping')
    d = arrow.utcnow().replace(microsecond=0)
    d_str = to_iso8601_datetime(d)
    d2 = from_iso8601_datetime(d_str)
    assert_that(d, equal_to(d2))
