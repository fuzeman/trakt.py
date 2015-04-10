from tests.core.helpers import assert_url

from trakt import Trakt
import json
import pytest
import responses


def test_authorize_url():
    with Trakt.configuration.client('mock', 'mock'):
        assert_url(Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob'), '/oauth/authorize', {
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'response_type': 'code',
            'client_id': 'mock'
        })

        assert_url(Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob', state='state', username='username'), '/oauth/authorize', {
            'username': 'username',
            'state': 'state',

            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'response_type': 'code',
            'client_id': 'mock'
        })

    with pytest.raises(ValueError):
        Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob')


def test_pin_url():
    with Trakt.configuration.app(id=1234):
        assert_url(Trakt['oauth'].pin_url(), '/pin/1234')

    with pytest.raises(ValueError):
        Trakt['oauth'].pin_url()


@responses.activate
def test_token_exchange():
    expected_request = {
        'client_secret': 'mock-client_secret',
        'code': 'ABCD1234',
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'client_id': 'mock-client_id',
        'grant_type': 'authorization_code'
    }

    def callback(request):
        data = json.loads(request.body)

        if data != expected_request:
            return 403, {}, ''

        return 200, {}, json.dumps({
            "access_token": "mock-access_token",
            "token_type": "bearer",
            "expires_in": 7200,
            "refresh_token": "mock-refresh_token",
            "scope": "public"
        })

    responses.add_callback(
        responses.POST, 'http://api.mock/oauth/token',
        callback=callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://api.mock'

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


@responses.activate
def test_token_refresh():
    expected_request = {
        'client_secret': 'mock-client_secret',
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'client_id': 'mock-client_id',
        'refresh_token': 'mock-refresh_token',
        'grant_type': 'refresh_token'
    }

    def callback(request):
        data = json.loads(request.body)

        if data != expected_request:
            return 403, {}, ''

        return 200, {}, json.dumps({
            "access_token": "mock-access_token",
            "token_type": "bearer",
            "expires_in": 7200,
            "refresh_token": "mock-refresh_token",
            "scope": "public"
        })

    responses.add_callback(
        responses.POST, 'http://api.mock/oauth/token',
        callback=callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://api.mock'

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
