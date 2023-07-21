
from tests.core import mock
from trakt import Trakt

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import assert_that, equal_to, has_entries, has_properties
from httmock import HTTMock


def assert_valid_show(hidden_item):
    assert_that(hidden_item, has_properties({
        'hidden_at': datetime(2015, 3, 30, 23, 18, 42, tzinfo=tzutc()),
        'hidden_type': 'show'
    }))
    assert hidden_item.hidden_item is not None
    assert_that(hidden_item.hidden_item.to_dict(), has_entries({
        'title': 'Gossip Girl',
        'year': 2007,
        'ids': {
            'tvdb': '80547',
            'tmdb': '1395',
            'imdb': 'tt0397442',
            'slug': 'gossip-girl',
            'trakt': '48'
        }
    }))


def assert_valid_movie(hidden_item):
    assert_that(hidden_item, has_properties({
        'hidden_at': datetime(2015, 6, 24, 5, 50, 21, tzinfo=tzutc()),
        'hidden_type': 'movie'
    }))
    assert hidden_item.hidden_item is not None
    assert_that(hidden_item.hidden_item.to_dict(), has_entries({
        'title': 'Mad Max: Fury Road',
        'year': 2015,
        'ids': {
            'trakt': '56360',
            'slug': 'mad-max-fury-road-2015',
            'imdb': 'tt1392190',
            'tmdb': '76341'
        }
    }))


def assert_valid_season(hidden_item):
    assert_that(hidden_item, has_properties({
        'hidden_at': datetime(2023, 3, 29, 10, 46, 20, tzinfo=tzutc()),
        'hidden_type': 'season'
    }))
    assert hidden_item.hidden_item is not None
    assert_that(hidden_item.hidden_item.to_dict(), has_entries({
        'number': 1,
        'ids': {
            'trakt': '260038',
            'tmdb': '198941'
        }
    }))
    assert hidden_item.show is not None
    assert_that(hidden_item.show.to_dict(), has_entries({
        'title': 'The Wonder Years',
        'year': 2021,
        'ids': {
            'trakt': '182038',
            'slug': 'the-wonder-years-2021',
            'tvdb': '402907',
            'imdb': 'tt12682076',
            'tmdb': '126164'
        }
    }))


def assert_valid_user(hidden_item):
    # {
    #   "user": {
    #     'username': 'sean',
    #     'private': false,
    #     'name': '',
    #     'vip': false,
    #     'vip_ep': false,
    #     'ids': {
    #       'slug': 'sean'
    #     }
    #   }
    # }
    assert_that(hidden_item, has_properties({
        'hidden_at': datetime(2023, 3, 29, 10, 58, 34, tzinfo=tzutc()),
        'hidden_type': 'user'
    }))
    assert hidden_item.hidden_item is not None
    assert_that(hidden_item.hidden_item, has_properties({
        'username': 'sean',
        'private': False,
        'name': '',
        'vip': False,
        'vip_ep': False,
        'pk': ('slug', 'sean')
    }))


def test_hidden_in_calendar():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/calendar'].get()
    assert_that(len(hidden_items), equal_to(2))
    assert_valid_show(hidden_items[0])
    assert_valid_movie(hidden_items[1])


def test_hidden_shows_in_calendar():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/calendar'].get(type='show')
    assert_that(len(hidden_items), equal_to(1))
    assert_valid_show(hidden_items[0])


def test_hidden_movies_in_calendar():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/calendar'].get(type='movie')
    assert_that(len(hidden_items), equal_to(1))
    assert_valid_movie(hidden_items[0])


def test_hidden_in_progress_watched():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/progress_watched'].get()
    assert_that(len(hidden_items), equal_to(2))
    assert_valid_show(hidden_items[0])
    assert_valid_season(hidden_items[1])


def test_hidden_shows_in_progress_watched():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/progress_watched'].get(type='show')
    assert_that(len(hidden_items), equal_to(1))
    assert_valid_show(hidden_items[0])


def test_hidden_seasons_in_progress_watched():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/progress_watched'].get(type='season')
    assert_that(len(hidden_items), equal_to(1))
    assert_valid_season(hidden_items[0])


def test_hidden_in_progress_collected():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/progress_collected'].get()
    assert_that(len(hidden_items), equal_to(2))
    assert_valid_show(hidden_items[0])
    assert_valid_season(hidden_items[1])


def test_hidden_shows_in_progress_collected():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/progress_collected'].get(type='show')
    assert_that(len(hidden_items), equal_to(1))
    assert_valid_show(hidden_items[0])


def test_hidden_seasons_in_progress_collected():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/progress_collected'].get(type='season')
    assert_that(len(hidden_items), equal_to(1))
    assert_valid_season(hidden_items[0])


def test_hidden_in_recommendations():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/recommendations'].get()
    assert_that(len(hidden_items), equal_to(2))
    assert_valid_show(hidden_items[0])
    assert_valid_movie(hidden_items[1])


def test_hidden_shows_in_recommendations():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/recommendations'].get(type='show')
    assert_that(len(hidden_items), equal_to(1))
    assert_valid_show(hidden_items[0])


def test_hidden_movies_in_recommendations():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/recommendations'].get(type='movie')
    assert_that(len(hidden_items), equal_to(1))
    assert_valid_movie(hidden_items[0])


def test_hidden_users_in_comments():
    with HTTMock(mock.hidden_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            hidden_items = Trakt['users/hidden/comments'].get()
    assert_that(len(hidden_items), equal_to(1))
    assert_valid_user(hidden_items[0])
