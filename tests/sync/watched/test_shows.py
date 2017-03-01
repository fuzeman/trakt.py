# flake8: noqa: F403, F405

from tests.core.helpers import authenticated_response
from trakt import Trakt

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
import responses


@responses.activate
def test_watched():
    responses.add_callback(
        responses.GET, 'http://mock/sync/watched/shows',
        callback=authenticated_response('fixtures/sync/watched/shows.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        collection = Trakt['sync/watched'].shows()

    # Ensure collection is valid
    assert_that(collection, not_none())
    assert_that(collection, has_length(9))

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

                        'plays': 9,

                        # Timestamps
                        'last_watched_at': datetime(2015, 3, 10, 5, 21, 51, tzinfo=tzutc()),

                        # Flags
                        'is_watched': True
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
