# flake8: noqa: F403, F405

from tests.core.helpers import authenticated_response
from trakt import Trakt
from trakt.objects import Person

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
import responses


@responses.activate
def test_basic():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/people/items',
        callback=authenticated_response('fixtures/users/me/lists/people/items.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

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
