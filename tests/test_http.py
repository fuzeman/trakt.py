from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock
from requests.exceptions import ConnectionError
from threading import Event
import httmock
import pytest


def test_shows_updates():
    with HTTMock(mock.fixtures, mock.unknown):
        response = Trakt.http.get('/shows/updates')

    items = response.json()

    assert [item['show']['title'] for item in items] == [
        'The Pop Game',
        'The Pop Game',
        'Abandoned Engineering'
    ]


def test_show_progress_collection():
    # TODO Add missing fixture
    with HTTMock(mock.fixtures, mock.unknown):
        response = Trakt.http.get('/shows/tt0944947/progress/collection')

    data = response.json()

    assert data['aired'] == 10
    assert data['completed'] == 6


def test_exception():
    ev = Event()

    @httmock.all_requests
    def handler(url, request):
        if ev.is_set():
            return httmock.response(201, request=request)

        # Set event
        ev.set()

        # Raise error
        raise ConnectionError('Example')

    with HTTMock(handler):
        with pytest.raises(ConnectionError):
            Trakt.http.get('/test')


def test_exception_retry():
    ev = Event()

    @httmock.all_requests
    def handler(url, request):
        if ev.is_set():
            return httmock.response(201, request=request)

        # Set event
        ev.set()

        # Raise error
        raise ConnectionError('Example')

    with HTTMock(handler):
        with Trakt.configuration.http(retry=True):
            response = Trakt.http.get('/test')

    assert response.status_code == 201


def test_error():
    ev = Event()

    @httmock.all_requests
    def handler(url, request):
        if ev.is_set():
            return httmock.response(201, request=request)

        # Set event
        ev.set()

        # Return error
        return httmock.response(504, request=request)

    with HTTMock(handler):
        response = Trakt.http.get('/test')

    assert response.status_code == 504


def test_error_retry():
    ev = Event()

    @httmock.all_requests
    def handler(url, request):
        if ev.is_set():
            return httmock.response(201, request=request)

        # Set event
        ev.set()

        # Return error
        return httmock.response(504, request=request)

    with HTTMock(handler):
        with Trakt.configuration.http(retry=True):
            response = Trakt.http.get('/test')

    assert response.status_code == 201
