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
            collection = Trakt['sync/collection'].shows()

    # Ensure collection is valid
    assert_that(collection, not_none())
    assert_that(collection, has_length(4))

    # Chuck (2007)
    assert_that(collection[('tvdb', '80348')], has_properties({
        'pk': ('tvdb', '80348'),
        'title': 'Chuck',
        'year': 2007,

        # Seasons
        'seasons': all_of(
            has_length(1),
            has_entry(1, has_properties({
                # Episodes
                'episodes': all_of(
                    has_length(4),
                    has_entry(2, has_properties({
                        'pk': (1, 2),

                        # Timestamps
                        'collected_at': datetime(2013, 10, 11, 1, 59, 5, tzinfo=tzutc()),

                        # Flags
                        'is_collected': True,
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

    assert_that(collection[('tvdb', '80348')].to_dict(), has_entries({
        'title': 'Chuck',
        'year': 2007,

        # Keys
        'ids': {
            'trakt':  '1395',
            'slug':   'chuck',
            'tvdb':   '80348',
            'imdb':   'tt0934814',
            'tmdb':   '1404',
            'tvrage': '15614'
        }
    }))

    assert_that(collection[('tvdb', '80348')].seasons[1].to_dict(), has_entries({
        'number': 1,

        # Episodes
        'episodes': has_item(has_entries({
            'number': 2,

            # Timestamps
            'collected_at': '2013-10-11T01:59:05.000-00:00',

            # Flags
            'collected': 1,
        })),
    }))

    assert_that(collection[('tvdb', '80348')].seasons[1].episodes[2].to_dict(), has_entries({
        'number': 2,

        # Timestamps
        'collected_at': '2013-10-11T01:59:05.000-00:00',

        # Flags
        'collected': 1,
    }))
