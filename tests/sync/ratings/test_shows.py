from tests.core.helpers import authenticated_response

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
from trakt import Trakt
import responses


@responses.activate
def test_ratings():
    responses.add_callback(
        responses.GET, 'http://mock/sync/ratings/shows',
        callback=authenticated_response('fixtures/sync/ratings/shows.json'),
        content_type='application/json'
    )

    responses.add_callback(
        responses.GET, 'http://mock/sync/ratings/seasons',
        callback=authenticated_response('fixtures/sync/ratings/seasons.json'),
        content_type='application/json'
    )

    responses.add_callback(
        responses.GET, 'http://mock/sync/ratings/episodes',
        callback=authenticated_response('fixtures/sync/ratings/episodes.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    collection = {}

    with Trakt.configuration.auth('mock', 'mock'):
        Trakt['sync/ratings'].shows(collection)
        Trakt['sync/ratings'].seasons(collection)
        Trakt['sync/ratings'].episodes(collection)

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
