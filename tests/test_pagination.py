# flake8: noqa: E241

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock


def test_iterator():
    with HTTMock(mock.lists, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            lists = Trakt['users/me/lists'].get(pagination=True)

            # Resolve all pages
            items = list(lists)

    # Ensure items were returned correctly
    assert [int(i.id) for i in items] == list(range(1, 38))


def test_invalid_content_type():
    with HTTMock(mock.lists_invalid_content_type, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            lists = Trakt['users/me/lists'].get(pagination=True)

            # Resolve all pages
            items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 0


def test_invalid_json():
    with HTTMock(mock.lists_invalid_json, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            lists = Trakt['users/me/lists'].get(pagination=True)

            # Resolve all pages
            items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 10


def test_request_failure():
    with HTTMock(mock.lists_request_failure, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            lists = Trakt['users/me/lists'].get(pagination=True)

            # Resolve all pages
            items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 10
