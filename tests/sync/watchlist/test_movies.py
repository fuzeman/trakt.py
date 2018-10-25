# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt
from trakt.objects import Movie, Show, Season, Episode

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
from httmock import HTTMock


def test_pagination_disabled():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            watchlist = Trakt['sync/watchlist'].movies(page=None, per_page=None)

    # Ensure collection is valid
    assert_that(watchlist, not_none())

    # Retrieve values from dictionary
    items = watchlist.values()

    # Validate items
    assert_that(items, contains(
        # TRON: Legacy (2010)
        all_of(
            instance_of(Movie),
            has_properties({
                'pk': ('imdb', 'tt1104001'),
                'title': 'TRON: Legacy',
                'year': 2010,

                # Timestamps
                'listed_at': datetime(2014, 9, 1, 9, 10, 11, tzinfo=tzutc()),

                # Keys
                'keys': [
                    ('imdb',  'tt1104001'),
                    ('tmdb',  '20526'),
                    ('slug',  'tron-legacy-2010'),
                    ('trakt', '1')
                ]
            })
        )
    ))
