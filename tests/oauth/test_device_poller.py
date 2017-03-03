from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock
from threading import Event
import httmock
import json
import pytest


class State:
    count = 0


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path='/oauth/device/token')
def oauth_device_token(url, request):
    assert request.body

    # Validate request body
    data = json.loads(request.body)

    assert data.get('client_id') == 'mock-client_id'
    assert data.get('client_secret') == 'mock-client_secret'
    assert data.get('code') == 'mock-device_code'

    # Return unauthenticated response
    if State.count < 5:
        return httmock.response(403, '', {
            'Content-Type': 'application/json'
        })

    # Return mock token
    return mock.oauth_device_token(url, request)


def test_expired():
    expired = Event()

    def on_expired():
        expired.set()

    with HTTMock(mock.fixtures, mock.unknown):
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

    with HTTMock(mock.fixtures, mock.unknown):
        # Construct poller
        poller = Trakt['oauth/device'].poll('mock-device_code', 600, 5)
        poller.on('aborted', on_aborted)

        # Start poller
        poller.start()

        # Ensure "aborted" event was fired
        aborted.wait(3)

        assert aborted.is_set() is True


def test_poll_authenticated():
    authenticated = Event()

    def on_authenticated(token):
        if not token:
            return

        authenticated.set()

    def on_poll(cb):
        State.count += 1

        cb()

    State.count = 0

    with HTTMock(oauth_device_token, mock.unknown):
        # Construct poller
        poller = Trakt['oauth/device'].poll('mock-device_code', 600, 1)
        poller.on('authenticated', on_authenticated)
        poller.on('poll', on_poll)

        # Start poller
        poller.start()

        # Ensure "authenticated" event was fired
        authenticated.wait(10)

        assert authenticated.is_set() is True


def test_poll_expired():
    expired = Event()

    def on_expired():
        expired.set()

    def on_poll(cb):
        State.count += 1

        cb()

    State.count = 0

    with HTTMock(oauth_device_token, mock.unknown):
        # Construct poller
        poller = Trakt['oauth/device'].poll('mock-device_code', 2, 1)
        poller.on('expired', on_expired)
        poller.on('poll', on_poll)

        # Start poller
        poller.start()

        # Ensure "authenticated" event was fired
        expired.wait(10)

        assert expired.is_set() is True


def test_double_start():
    with HTTMock(mock.fixtures, mock.unknown):
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
