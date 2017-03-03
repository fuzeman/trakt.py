from __future__ import absolute_import, division, print_function

from tests.core.helpers import assert_url
from trakt import Trakt

import pytest


def test_url():
    with Trakt.configuration.app(id=1234):
        assert_url(Trakt['oauth/pin'].url(), '/pin/1234')

    with pytest.raises(ValueError):
        Trakt['oauth/pin'].url()
