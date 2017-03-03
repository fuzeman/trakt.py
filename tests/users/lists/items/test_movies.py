# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt
from trakt.objects import Movie

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
from httmock import HTTMock


def test_basic():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['users/me/lists/movies'].items()

    # Ensure collection is valid
    assert_that(items, not_none())

    # Validate items
    assert_that(items, contains(
        # Mad Max: Fury Road
        all_of(
            instance_of(Movie),
            has_properties({
                'pk': ('imdb', 'tt1392190'),
                'title': 'Mad Max: Fury Road',
                'year': 2015,

                # Timestamps
                'listed_at': datetime(2015, 6, 24, 5, 50, 21, tzinfo=tzutc()),

                # Keys
                'keys': [
                    ('imdb', 'tt1392190'),
                    ('tmdb', '76341'),
                    ('slug', 'mad-max-fury-road-2015'),
                    ('trakt', '56360')
                ]
            })
        ),

        # Maggie (2015)
        all_of(
            instance_of(Movie),
            has_properties({
                'pk': ('imdb', 'tt1881002'),
                'title': 'Maggie',
                'year': 2015,

                # Timestamps
                'listed_at': datetime(2015, 6, 24, 5, 50, 21, tzinfo=tzutc()),

                # Keys
                'keys': [
                    ('imdb', 'tt1881002'),
                    ('tmdb', '287424'),
                    ('slug', 'maggie-1969'),
                    ('trakt', '184504')
                ]
            })
        )
    ))
