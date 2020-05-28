# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
from httmock import HTTMock


def test_ratings():
    with HTTMock(mock.fixtures, mock.unknown):
        collection = {}

        with Trakt.configuration.auth('mock', 'mock'):
            Trakt['sync/ratings'].shows(store=collection)
            Trakt['sync/ratings'].seasons(store=collection)
            Trakt['sync/ratings'].episodes(store=collection)

    # Ensure collection is valid
    assert_that(collection, not_none())
    assert_that(collection, has_length(6))

    # Chuck (2007)
    assert_that(collection[('tvdb', '80348')], has_properties({
        'pk': ('tvdb', '80348'),
        'title': 'Chuck',
        'year': 2007,

        'rating': has_properties({
            'value': 10,
            'votes': None,
            'timestamp': datetime(2014, 10, 19, 23, 2, 23, tzinfo=tzutc())
        }),

        # Seasons
        'seasons': all_of(
            has_length(1),
            has_entry(1, has_properties({
                'pk': 1,

                # Rating
                'rating': has_properties({
                    'value': 10,
                    'votes': None,
                    'timestamp': datetime(2015, 3, 11, 23, 29, 35, tzinfo=tzutc())
                }),

                # Episodes
                'episodes': all_of(
                    has_length(1),
                    has_entry(1, has_properties({
                        'pk': (1, 1),

                        # Rating
                        'rating': has_properties({
                            'value': 10,
                            'votes': None,
                            'timestamp': datetime(2014, 10, 19, 23, 2, 24, tzinfo=tzutc())
                        }),

                        # Keys
                        'keys': [
                            (1, 1),
                            ('tvdb', '332179'),
                            ('tmdb', '63425'),
                            ('tvrage', '579282'),
                            ('trakt', '74041')
                        ]
                    }))
                ),

                # Keys
                'keys': [
                    1,
                    ('tvdb', '27985'),
                    ('tmdb', '3650'),
                    ('trakt', '3993')
                ]
            })),
        ),

        # Keys
        'keys': [
            ('tvdb', '80348'),
            ('tmdb', '1404'),
            ('imdb', 'tt0934814'),
            ('tvrage', '15614'),
            ('slug', 'chuck'),
            ('trakt', '1395')
        ]
    }))
