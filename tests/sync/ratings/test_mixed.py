# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt
from trakt.objects import Movie, Show, Season, Episode

from hamcrest import *
from httmock import HTTMock


def test_basic():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            ratings = Trakt['sync/ratings'].get()

    # Ensure collection is valid
    assert_that(ratings, not_none())

    # Resolve all pages
    items = list(ratings)

    # Verify items
    assert_that(items, all_of(
        has_length(4),

        # TRON: Legacy (2010)
        has_item(all_of(
            instance_of(Movie),
            has_properties({
                'pk': ('imdb', 'tt1104001')
            })
        )),

        # Breaking Bad (2008)
        has_item(all_of(
            instance_of(Show),
            has_properties({
                'pk': ('tvdb', '81189')
            })
        )),

        # Breaking Bad (2008) - S00
        has_item(all_of(
            instance_of(Season),
            has_properties({
                'pk': 0
            })
        )),

        # Breaking Bad (2008) - S04E01
        has_item(all_of(
            instance_of(Episode),
            has_properties({
                'pk': (4, 1)
            })
        ))
    ))
