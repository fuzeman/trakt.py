from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock
import pytest


def test_get():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):

            with pytest.raises(ValueError):
                items = Trakt['users/*/watched'].get('me')

            with pytest.raises(ValueError):
                items = Trakt['users/*/watched'].get('me', 'episodes')

            items = Trakt['users/*/watched'].get('me', 'shows')

            assert items is not None

            items = list(items)

            assert len(items) == 2

            assert items[0] is not None

            assert items[1] is not None

            assert items[0].title == 'Breaking Bad'

            assert items[0].keys == [
                ('tvdb', '81189'),
                ('tmdb', '1396'),
                ('imdb', 'tt0903747'),
                ('slug', 'breaking-bad'),
                ('trakt', '1')
            ]

            assert items[1].title == 'Parks and Recreation'

            items = Trakt['users/*/watched'].get('me', 'movies')

            assert items is not None

            items = list(items)

            assert len(items) == 2

            assert items[0] is not None

            assert items[1] is not None

            assert items[0].title == 'Batman Begins'

            assert items[1].title == 'The Dark Knight'

            assert items[1].keys == [
                ('imdb', 'tt0468569'),
                ('tmdb', '155'),
                ('slug', 'the-dark-knight-2008'),
                ('trakt', '4')
            ]
