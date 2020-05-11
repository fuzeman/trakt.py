# flake8: noqa: E241

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock


def test_iterator():
    with HTTMock(mock.likes, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            lists = Trakt['users'].likes(pagination=True)

            # Resolve all pages
            items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 3


def test_invalid_content_type():
    with HTTMock(mock.likes_invalid_content_type, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            lists = Trakt['users'].likes(pagination=True)

            # Resolve all pages
            items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 0


def test_invalid_json():
    with HTTMock(mock.likes_invalid_json, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            lists = Trakt['users'].likes(pagination=True, per_page=1)

            # Resolve all pages
            items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 1


def test_request_failure():
    with HTTMock(mock.likes_request_failure, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            lists = Trakt['users'].likes(pagination=True, per_page=1)

            # Resolve all pages
            items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 1
