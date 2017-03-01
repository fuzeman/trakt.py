from trakt import Trakt

import json
import pytest
import responses


@responses.activate
def test_code():
    expected_request = {
        'client_id': 'mock-client_id'
    }

    def callback(request):
        data = json.loads(request.body)

        if data != expected_request:
            return 403, {}, ''

        return 200, {}, json.dumps({
            "device_code": "mock-device_code",
            "user_code": "mock-user_code",
            "verification_url": "https://trakt.tv/activate",
            "expires_in": 600,
            "interval": 5
        })

    responses.add_callback(
        responses.POST, 'http://api.mock/oauth/device/code',
        callback=callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://api.mock'

    # Validate `code` request/response
    with Trakt.configuration.client('mock-client_id', 'mock-client_secret'):
        assert Trakt['oauth/device'].code() == {
            "device_code": "mock-device_code",
            "user_code": "mock-user_code",
            "verification_url": "https://trakt.tv/activate",
            "expires_in": 600,
            "interval": 5
        }

    # Ensure `code` raises a `ValueError` on incorrect configuration
    with pytest.raises(ValueError):
        assert Trakt['oauth/device'].code()


@responses.activate
def test_token():
    expected_request = {
        'client_id': 'mock-client_id',
        'client_secret': 'mock-client_secret',

        'code': 'mock-device_code'
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
        responses.POST, 'http://api.mock/oauth/device/token',
        callback=callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://api.mock'

    # Validate `token` request/response
    with Trakt.configuration.client('mock-client_id', 'mock-client_secret'):
        assert Trakt['oauth/device'].token('mock-device_code') == {
            "access_token": "mock-access_token",
            "token_type": "bearer",
            "expires_in": 7200,
            "refresh_token": "mock-refresh_token",
            "scope": "public"
        }

    # Ensure `token` raises a `ValueError` on incorrect configuration
    with pytest.raises(ValueError):
        assert Trakt['oauth/device'].token('mock-device_code')
