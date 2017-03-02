from tests.core import mock
from tests.core.helpers import assert_url
from trakt import Trakt, TraktClient

from httmock import HTTMock
from threading import Event
import calendar
import datetime
import pytest


def test_authorize_url():
    Trakt.site_url = 'http://mock'

    with Trakt.configuration.client('mock', 'mock'):
        assert_url(Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob'), '/oauth/authorize', {
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'response_type': 'code',
            'client_id': 'mock'
        })

        assert_url(
            Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob', state='state', username='username'),
            '/oauth/authorize', {
                'username': 'username',
                'state': 'state',

                'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
                'response_type': 'code',
                'client_id': 'mock'
            }
        )

    with pytest.raises(ValueError):
        Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob')


def test_pin_url():
    with Trakt.configuration.app(id=1234):
        assert_url(Trakt['oauth'].pin_url(), '/pin/1234')

    with pytest.raises(ValueError):
        Trakt['oauth'].pin_url()


def test_token():
    with HTTMock(mock.fixtures, mock.unknown):
        # Validate `token_exchange` request/response
        with Trakt.configuration.client('mock-client_id', 'mock-client_secret'):
            assert Trakt['oauth'].token('ABCD1234', 'urn:ietf:wg:oauth:2.0:oob') == {
                "access_token": "mock-access_token",
                "token_type": "bearer",
                "expires_in": 7200,
                "refresh_token": "mock-refresh_token",
                "scope": "public"
            }

        # Ensure `token_exchange` raises a `ValueError` on incorrect configuration
        with pytest.raises(ValueError):
            assert Trakt['oauth'].token('ABCD1234', 'urn:ietf:wg:oauth:2.0:oob')


def test_token_exchange():
    with HTTMock(mock.fixtures, mock.unknown):
        # Validate `token_exchange` request/response
        with Trakt.configuration.client('mock-client_id', 'mock-client_secret'):
            assert Trakt['oauth'].token_exchange('ABCD1234', 'urn:ietf:wg:oauth:2.0:oob') == {
                "access_token": "mock-access_token",
                "token_type": "bearer",
                "expires_in": 7200,
                "refresh_token": "mock-refresh_token",
                "scope": "public"
            }

        # Ensure `token_exchange` raises a `ValueError` on incorrect configuration
        with pytest.raises(ValueError):
            assert Trakt['oauth'].token_exchange('ABCD1234', 'urn:ietf:wg:oauth:2.0:oob')


def test_token_refresh():
    with HTTMock(mock.fixtures, mock.unknown):
        # Validate `token_exchange` request/response
        with Trakt.configuration.client('mock-client_id', 'mock-client_secret'):
            assert Trakt['oauth'].token_refresh('mock-refresh_token', 'urn:ietf:wg:oauth:2.0:oob') == {
                "access_token": "mock-access_token",
                "token_type": "bearer",
                "expires_in": 7200,
                "refresh_token": "mock-refresh_token",
                "scope": "public"
            }

        # Ensure `token_exchange` raises a `ValueError` on incorrect configuration
        with pytest.raises(ValueError):
            assert Trakt['oauth'].token_refresh('mock-refresh_token', 'urn:ietf:wg:oauth:2.0:oob')


def test_request():
    with HTTMock(mock.fixtures, mock.unknown):
        # Mock authorization
        authorization = {
            "access_token": "mock",
            "token_type": "bearer",
            "created_at": calendar.timegm(datetime.datetime.utcnow().utctimetuple()),
            "expires_in": 7 * 24 * 60 * 60,
            "refresh_token": "mock-refresh_token",
            "scope": "public"
        }

        # Test valid token
        with Trakt.configuration.oauth.from_response(authorization):
            assert Trakt['sync/collection'].movies() is not None

        # Test expired token
        authorization['expires_in'] = 0

        with Trakt.configuration.oauth.from_response(authorization):
            assert Trakt['sync/collection'].movies() is None

        # Test token refreshing
        with Trakt.configuration\
                .client('mock', 'mock')\
                .oauth.from_response(authorization, refresh=True):
            assert Trakt['sync/collection'].movies() is not None


def test_refresh_deadlock():
    with HTTMock(mock.fixtures, mock.unknown):
        # Construct client
        client = TraktClient()

        # Configure client
        client.configuration.defaults.client(
            id='mock',
            secret='mock'
        )

        # Bind to events
        refreshed = Event()
        looped = Event()

        @client.on('oauth.refresh')
        def on_token_refreshed(username, authorization):
            if refreshed.is_set():
                looped.set()
                return

            refreshed.set()

            # Test refresh recursion
            assert client['sync/collection'].movies() is None

        # Attempt request with expired authorization
        expired_authorization = {
            "access_token": "mock",
            "token_type": "bearer",
            "created_at": calendar.timegm(datetime.datetime.utcnow().utctimetuple()),
            "expires_in": 0,
            "refresh_token": "mock",
            "scope": "public"
        }

        with client.configuration.oauth.from_response(expired_authorization, refresh=True, username='mock'):
            assert client['sync/collection'].movies() is not None

        # Ensure requests inside "oauth.refresh" don't cause refresh loops
        assert not looped.is_set()
