# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt
from trakt.objects import Movie, Show, Season, Episode

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
from httmock import HTTMock


def test_basic():
    with HTTMock(mock.sync_watchlist, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            watchlist = Trakt['sync/watchlist'].get(pagination=True, per_page=3)

            # Ensure collection is valid
            assert_that(watchlist, not_none())

            # Resolve all pages
            items = list(watchlist)

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
        ),

        # Breaking Bad (2008)
        all_of(
            instance_of(Show),
            has_properties({
                'pk': ('tvdb', '81189'),
                'title': 'Breaking Bad',
                'year': 2008,

                # Timestamps
                'listed_at': datetime(2014, 9, 1, 9, 10, 11, tzinfo=tzutc()),

                # Keys
                'keys': [
                    ('tvdb', '81189'),
                    ('tmdb', '1396'),
                    ('imdb', 'tt0903747'),
                    ('tvrage', '18164'),
                    ('slug', 'breaking-bad'),
                    ('trakt', '1')
                ]
            })
        ),

        # Breaking Bad (2008) - S03
        all_of(
            instance_of(Season),
            has_properties({
                'pk': 3,

                # Timestamps
                'listed_at': datetime(2014, 9, 1, 9, 10, 11, tzinfo=tzutc()),

                # Keys
                'keys': [
                    3,
                    ('tvdb', '171641'),
                    ('tmdb', '3575')
                ]
            })
        ),

        # Breaking Bad (2008) - S04E01
        all_of(
            instance_of(Episode),
            has_properties({
                'pk': (4, 1),
                'title': 'Box Cutter',

                # Timestamps
                'listed_at': datetime(2014, 9, 1, 9, 10, 11, tzinfo=tzutc()),

                # Keys
                'keys': [
                    (4, 1),
                    ('tvdb', '2639411'),
                    ('tmdb', '62118'),
                    ('imdb', 'tt1683084'),
                    ('trakt', '49')
                ]
            })
        )
    ))


def test_pagination_disabled():
    with HTTMock(mock.sync_watchlist, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            watchlist = Trakt['sync/watchlist'].get(page=None, per_page=None)

            # Ensure collection is valid
            assert_that(watchlist, not_none())

            # Resolve iterator
            items = list(watchlist)

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
        ),

        # Breaking Bad (2008)
        all_of(
            instance_of(Show),
            has_properties({
                'pk': ('tvdb', '81189'),
                'title': 'Breaking Bad',
                'year': 2008,

                # Timestamps
                'listed_at': datetime(2014, 9, 1, 9, 10, 11, tzinfo=tzutc()),

                # Keys
                'keys': [
                    ('tvdb', '81189'),
                    ('tmdb', '1396'),
                    ('imdb', 'tt0903747'),
                    ('tvrage', '18164'),
                    ('slug', 'breaking-bad'),
                    ('trakt', '1')
                ]
            })
        ),

        # Breaking Bad (2008) - S03
        all_of(
            instance_of(Season),
            has_properties({
                'pk': 3,

                # Timestamps
                'listed_at': datetime(2014, 9, 1, 9, 10, 11, tzinfo=tzutc()),

                # Keys
                'keys': [
                    3,
                    ('tvdb', '171641'),
                    ('tmdb', '3575')
                ]
            })
        ),

        # Breaking Bad (2008) - S04E01
        all_of(
            instance_of(Episode),
            has_properties({
                'pk': (4, 1),
                'title': 'Box Cutter',

                # Timestamps
                'listed_at': datetime(2014, 9, 1, 9, 10, 11, tzinfo=tzutc()),

                # Keys
                'keys': [
                    (4, 1),
                    ('tvdb', '2639411'),
                    ('tmdb', '62118'),
                    ('imdb', 'tt1683084'),
                    ('trakt', '49')
                ]
            })
        )
    ))
