# flake8: noqa: F403, F405

from tests.core.helpers import authenticated_response
from trakt import Trakt

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
import responses


@responses.activate
def test_basic():
    responses.add_callback(
        responses.GET, 'http://mock/sync/ratings/movies',
        callback=authenticated_response('fixtures/sync/ratings/movies.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        collection = Trakt['sync/ratings'].movies()

    # Ensure collection is valid
    assert_that(collection, not_none())

    # 100 Bloody Acres (2012)
    assert_that(collection[('imdb', 'tt2290065')], has_properties({
        'pk': ('imdb', 'tt2290065'),
        'title': '100 Bloody Acres',
        'year': 2012,

        'rating': has_properties({
            'value': 8,
            'timestamp': datetime(2015, 1, 28, 2, 26, 37, tzinfo=tzutc())
        }),

        # Keys
        'keys': [
            ('imdb', 'tt2290065'),
            ('tmdb', '126757'),
            ('slug', '100-bloody-acres-2012'),
            ('trakt', '86920')
        ]
    }))

    # The Hobbit: The Desolation of Smaug (2013)
    assert_that(collection[('imdb', 'tt1170358')], has_properties({
        'pk': ('imdb', 'tt1170358'),
        'title': 'The Hobbit: The Desolation of Smaug',
        'year': 2013,

        'rating': has_properties({
            'value': 10,
            'timestamp': datetime(2014, 11, 1, 0, 24, 54, tzinfo=tzutc())
        }),

        # Keys
        'keys': [
            ('imdb', 'tt1170358'),
            ('tmdb', '57158'),
            ('slug', 'the-hobbit-the-desolation-of-smaug-2013'),
            ('trakt', '40808')
        ]
    }))


@responses.activate
def test_rating_filter():
    responses.add_callback(
        responses.GET, 'http://mock/sync/ratings/movies/8',
        callback=authenticated_response('fixtures/sync/ratings/movies/8.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        collection = Trakt['sync/ratings'].movies(rating=8)

    # Ensure collection is valid
    assert_that(collection, not_none())
    assert_that(collection, has_length(1))

    # 100 Bloody Acres (2012)
    assert_that(collection[('imdb', 'tt2290065')], has_properties({
        'pk': ('imdb', 'tt2290065'),
        'title': '100 Bloody Acres',
        'year': 2012,

        'rating': has_properties({
            'value': 8,
            'timestamp': datetime(2015, 1, 28, 2, 26, 37, tzinfo=tzutc())
        }),

        # Keys
        'keys': [
            ('imdb', 'tt2290065'),
            ('tmdb', '126757'),
            ('slug', '100-bloody-acres-2012'),
            ('trakt', '86920')
        ]
    }))
