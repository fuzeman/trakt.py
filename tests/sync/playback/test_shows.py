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
            collection = Trakt['sync/playback'].episodes()

    # Ensure collection is valid
    assert_that(collection, not_none())

    # Chuck (2007)
    assert_that(collection[('tvdb', '80348')], has_properties({
        'pk': ('tvdb', '80348'),
        'title': 'Chuck',
        'year': 2007,

        # Seasons
        'seasons': all_of(
            has_length(1),

            # Seasons
            has_entry(1, has_properties({
                'episodes': all_of(
                    has_length(2),

                    # Episodes
                    has_entry(3, has_properties({
                        'pk': (1, 3),
                        'title': 'Chuck Versus the Tango',

                        'progress': 4.99,

                        # Timestamps
                        'paused_at': datetime(2015, 3, 9, 0, 10, 15, tzinfo=tzutc()),

                        # Keys
                        'keys': [
                            (1, 3),
                            ('tvdb', '336271'),
                            ('tmdb', '63434'),
                            ('tvrage', '595113'),
                            ('trakt', '74043')
                        ]
                    }))
                )
            }))
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
