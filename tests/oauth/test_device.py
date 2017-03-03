from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt, TraktClient

from httmock import HTTMock
import pytest


def test_code():
    with HTTMock(mock.oauth_device_code, mock.unknown):
        # Validate `code` request/response
        assert Trakt['oauth/device'].code() == {
            'device_code': 'mock-device_code',
            'user_code': 'mock-user_code',
            'verification_url': 'https://trakt.tv/activate',
            'expires_in': 600,
            'interval': 5
        }

        # Ensure `code` raises a `ValueError` on incorrect configuration
        with pytest.raises(ValueError):
            assert TraktClient()['oauth/device'].code()


def test_token():
    with HTTMock(mock.oauth_device_token, mock.unknown):
        # Validate `token` request/response
        assert Trakt['oauth/device'].token('mock-device_code') == {
            'access_token': 'mock-access_token',
            'token_type': 'bearer',
            'expires_in': 7200,
            'refresh_token': 'mock-refresh_token',
            'scope': 'public'
        }

        # Ensure `token` raises a `ValueError` on incorrect configuration
        with pytest.raises(ValueError):
            assert TraktClient()['oauth/device'].token('mock-device_code')
