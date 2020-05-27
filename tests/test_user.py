from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock
import datetime
import pytest


def test_likes():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            likes = Trakt['users'].likes()
            assert likes is not None

            likes = list(likes)

    assert len(likes) == 3

    assert likes[0].keys == [
        ('trakt', 1519)
    ]

    assert likes[1].keys == [
        ('trakt', '1238362'),
        ('slug', 'star-wars-machete')
    ]

    assert likes[2].keys == [
        ('trakt', '840781'),
        ('slug', 'star-wars-timeline')
    ]


def test_likes_invalid_response():
    with HTTMock(mock.fixtures, mock.unknown):
        likes = Trakt['users'].likes()

    assert likes is None


def test_likes_invalid_type():
    with HTTMock(mock.fixtures, mock.unknown):
        with pytest.raises(ValueError):
            likes = Trakt['users'].likes('invalid')
            assert likes is not None

            likes = list(likes)


def test_following():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            following = Trakt['users/*/following'].get('me')
            assert following is not None

            following = list(following)

            assert following[0].keys == [
                ('slug', 'sean')
            ]

            assert following[1].keys == [
                ('slug', 'justin')
            ]

            assert following[0].name == 'Sean Rudford'

            assert isinstance(following[0].followed_at, datetime.datetime)

            assert following[1].name == 'Justin Nemeth'


def test_friends():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            friends = Trakt['users/*/friends'].get('me')

            assert friends is not None

            friends = list(friends)

            assert friends[0].keys == [
                ('slug', 'sean')
            ]

            assert friends[1].keys == [
                ('slug', 'justin')
            ]

            assert isinstance(friends[0].friends_at, datetime.datetime)

            assert friends[0].name == 'Sean Rudford'

            assert friends[0].username == 'sean'


def test_history():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['users/*/history'].items('me')

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


def test_ratings():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['users/*/ratings'].items('me')

            assert items is not None

            items = list(items)

            assert len(items) == 2

            assert items[0] is not None
            assert items[1] is not None

            assert items[0].rating.value == 10

            assert isinstance(items[0].rating.timestamp, datetime.datetime)

            assert items[0].title == 'TRON: Legacy'


def test_watchlist():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['users/*/watchlist'].items('me')

            assert items is not None

            assert len(items) == 2

            assert items[0] is not None

            assert isinstance(items[0].listed_at, datetime.datetime)

            assert items[0].title == 'TRON: Legacy'
