# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt
from trakt.objects import Person

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
from httmock import HTTMock


def test_basic():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['users/me/lists/people'].items()

    # Ensure collection is valid
    assert_that(items, not_none())

    # Validate items
    assert_that(items, contains(
        # Bryan Cranston
        all_of(
            instance_of(Person),
            has_properties({
                'pk': ('tmdb', '17419'),
                'name': 'Bryan Cranston',

                # Timestamps
                'listed_at': datetime(2014, 6, 17, 6, 52, 3, tzinfo=tzutc()),

                # Keys
                'keys': [
                    ('tmdb', '17419'),
                    ('imdb', 'nm0186505'),
                    ('tvrage', '1797'),
                    ('slug', 'bryan-cranston'),
                    ('trakt', '1')
                ]
            })
        ),

        # Aaron Paul
        all_of(
            instance_of(Person),
            has_properties({
                'pk': ('tmdb', '84497'),
                'name': 'Aaron Paul',

                # Timestamps
                'listed_at': datetime(2014, 6, 17, 6, 52, 3, tzinfo=tzutc()),

                # Keys
                'keys': [
                    ('tmdb', '84497'),
                    ('imdb', 'nm0666739'),
                    ('tvrage', '1823'),
                    ('slug', 'aaron-paul'),
                    ('trakt', '415249')
                ]
            })
        )
    ))
