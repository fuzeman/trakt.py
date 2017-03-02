# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
from httmock import HTTMock


def test_basic():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            collection = Trakt['sync/collection'].movies()

    # Ensure collection is valid
    assert_that(collection, not_none())

    # TRON: Legacy (2010)
    assert_that(collection[('imdb', 'tt1104001')], has_properties({
        'pk': ('imdb', 'tt1104001'),
        'title': 'TRON: Legacy',
        'year': 2010,

        # Timestamps
        'collected_at': datetime(2014, 9, 28, 22, 45, 23, tzinfo=tzutc()),

        # Flags
        'is_collected': True,

        # Keys
        'keys': [
            ('imdb',  'tt1104001'),
            ('tmdb',  '20526'),
            ('slug',  'tron-legacy-2010'),
            ('trakt', '12601')
        ]
    }))

    assert_that(collection[('imdb', 'tt1104001')].to_dict(), has_entries({
        'title': 'TRON: Legacy',
        'year': 2010,

        # Timestamps
        'collected_at': '2014-09-28T22:45:23.000-00:00',

        # Flags
        'collected': 1,

        # Keys
        'ids': {
            'imdb':  'tt1104001',
            'tmdb':  '20526',
            'slug':  'tron-legacy-2010',
            'trakt': '12601'
        }
    }))

    # 100 Bloody Acres (2012)
    assert_that(collection[('imdb', 'tt2290065')], has_properties({
        'pk': ('imdb', 'tt2290065'),
        'title': '100 Bloody Acres',
        'year': 2012,

        # Timestamps
        'collected_at': datetime(2014, 1, 20, 7, 4, 4, tzinfo=tzutc()),

        # Flags
        'is_collected': True,

        # Keys
        'keys': [
            ('imdb',  'tt2290065'),
            ('tmdb',  '126757'),
            ('slug',  '100-bloody-acres-2012'),
            ('trakt', '86920')
        ]
    }))

    assert_that(collection[('imdb', 'tt2290065')].to_dict(), has_entries({
        'title': '100 Bloody Acres',
        'year': 2012,

        # Timestamps
        'collected_at': '2014-01-20T07:04:04.000-00:00',

        # Flags
        'collected': 1,

        # Keys
        'ids': {
            'imdb':  'tt2290065',
            'tmdb':  '126757',
            'slug':  '100-bloody-acres-2012',
            'trakt': '86920'
        }
    }))
