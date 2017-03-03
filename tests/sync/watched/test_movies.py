# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
from httmock import HTTMock


def test_watched():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            collection = Trakt['sync/watched'].movies()

    # Ensure collection is valid
    assert_that(collection, not_none())

    # 100 Bloody Acres (2012)
    assert_that(collection[('imdb', 'tt2290065')], has_properties({
        'pk': ('imdb', 'tt2290065'),
        'title': '100 Bloody Acres',
        'year': 2012,

        'plays': 2,

        # Timestamps
        'last_watched_at':  datetime(2014, 4, 27, 13, 43, 59, tzinfo=tzutc()),

        # Keys
        'keys': [
            ('imdb', 'tt2290065'),
            ('tmdb', '126757'),
            ('slug', '100-bloody-acres-2012'),
            ('trakt', '86920')
        ]
    }))

    # The Hobbit: The Desolation of Smaug (2013)
    assert_that(collection[('imdb', 'tt1170358')], has_properties({
        'pk': ('imdb', 'tt1170358'),
        'title': 'The Hobbit: The Desolation of Smaug',
        'year': 2013,

        'plays': 1,

        # Timestamps
        'last_watched_at': datetime(2014, 4, 20, 12, 32, 59, tzinfo=tzutc()),

        # Keys
        'keys': [
            ('imdb', 'tt1170358'),
            ('tmdb', '57158'),
            ('slug', 'the-hobbit-the-desolation-of-smaug-2013'),
            ('trakt', '40808')
        ]
    }))

    # TRON: Legacy (2010)
    assert_that(collection[('imdb', 'tt1104001')], has_properties({
        'pk': ('imdb', 'tt1104001'),
        'title': 'TRON: Legacy',
        'year': 2010,

        'plays': 1,

        # Timestamps
        'last_watched_at': datetime(2015, 1, 27, 23, 30, 16, tzinfo=tzutc()),

        # Keys
        'keys': [
            ('imdb',  'tt1104001'),
            ('tmdb',  '20526'),
            ('slug',  'tron-legacy-2010'),
            ('trakt', '12601')
        ]
    }))
