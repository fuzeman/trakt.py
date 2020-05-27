from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock
import datetime


def test_get():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['users/*/history'].get('me')

            assert items is not None

            items = list(items)

            assert len(items) == 3

            assert items[0] is not None

            assert items[1] is not None

            assert items[2] is not None

            assert isinstance(items[0].watched_at, datetime.datetime)

            assert items[0].title == 'The Dark Knight'

            assert items[0].keys == [
                ('imdb', 'tt0468569'),
                ('tmdb', '155'),
                ('slug', 'the-dark-knight-2008'),
                ('trakt', '4')
            ]

            assert items[1].title == 'Pawnee Zoo'
