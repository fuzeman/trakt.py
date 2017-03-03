# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
from httmock import HTTMock


def test_movies():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            value = Trakt['users/me/lists/movies'].get()

    # Validate movies list
    assert_that(value, has_properties({
        'name': 'Movies',
        'description': None,
        'likes': 0,

        'allow_comments': True,
        'display_numbers': False,

        'updated_at': datetime(2015, 6, 22, 2, 25, tzinfo=tzutc()),

        'comment_count': 0,
        'item_count': 2,

        'privacy': 'private'
    }))


def test_shows():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            value = Trakt['users/me/lists/shows'].get()

    # Validate shows list
    assert_that(value, has_properties({
        'name': 'Shows',
        'description': None,
        'likes': 0,

        'allow_comments': True,
        'display_numbers': False,

        'updated_at': datetime(2015, 6, 22, 2, 25, tzinfo=tzutc()),

        'comment_count': 0,
        'item_count': 3,

        'privacy': 'private'
    }))
