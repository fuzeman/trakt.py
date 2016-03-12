from threading import Event
from trakt import Trakt
import json
import pytest
import responses


def test_expired():
    expired = Event()

    def on_expired():
        expired.set()

    # Setup client
    Trakt.base_url = 'http://api.mock'

    # Construct poller
    poller = Trakt['oauth/device'].poll('mock-device_code', -5, 5)
    poller.on('expired', on_expired)

    # Start poller
    poller.start()

    # Ensure "expired" event was fired
    expired.wait(3)

    assert expired.is_set() is True


def test_aborted():
    aborted = Event()

    def on_aborted():
        aborted.set()

    # Setup client
    Trakt.base_url = 'http://api.mock'

    # Construct poller
    poller = Trakt['oauth/device'].poll('mock-device_code', 600, 5)
    poller.on('aborted', on_aborted)

    # Start poller
    poller.start()

    # Ensure "aborted" event was fired
    aborted.wait(3)

    assert aborted.is_set() is True


@responses.activate
def test_poll_authenticated():
    class state:
        count = 0

    def callback(request):
        if state.count < 5:
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

    authenticated = Event()

    def on_authenticated(token):
        if not token:
            return

        authenticated.set()

    def on_poll(cb):
        state.count += 1

        cb()

    # Setup client
    Trakt.base_url = 'http://api.mock'

    # Construct poller
    poller = Trakt['oauth/device'].poll('mock-device_code', 600, 1)
    poller.on('authenticated', on_authenticated)
    poller.on('poll', on_poll)

    # Set client configuration
    Trakt.configuration.defaults.client('mock-client_id', 'mock-client_secret')

    try:
        # Start poller
        poller.start()

        # Ensure "authenticated" event was fired
        authenticated.wait(10)

        assert authenticated.is_set() is True
    finally:
        # Reset client configuration
        Trakt.configuration.defaults.client()


@responses.activate
def test_poll_expired():
    class state:
        count = 0

    def callback(request):
        if state.count < 5:
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

    expired = Event()

    def on_expired():
        expired.set()

    def on_poll(cb):
        state.count += 1

        cb()

    # Setup client
    Trakt.base_url = 'http://api.mock'

    # Construct poller
    poller = Trakt['oauth/device'].poll('mock-device_code', 2, 1)
    poller.on('expired', on_expired)
    poller.on('poll', on_poll)

    # Set client configuration
    Trakt.configuration.defaults.client('mock-client_id', 'mock-client_secret')

    try:
        # Start poller
        poller.start()

        # Ensure "authenticated" event was fired
        expired.wait(10)

        assert expired.is_set() is True
    finally:
        # Reset client configuration
        Trakt.configuration.defaults.client()


def test_double_start():
    # Setup client
    Trakt.base_url = 'http://api.mock'

    # Construct poller
    poller = Trakt['oauth/device'].poll('mock-device_code', 600, 5)

    # Start poller
    poller.start()

    try:
        # Ensure an exception is raised when attempting to start the poller again
        with pytest.raises(Exception):
            poller.start()
    finally:
        # Stop polling
        poller.stop()
