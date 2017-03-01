# flake8: noqa: F403, F405

from tests.core.helpers import authenticated_response
from trakt import Trakt

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
import responses


@responses.activate
def test_movies():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/movies',
        callback=authenticated_response('fixtures/users/me/lists/movies.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        value = Trakt['users/me/lists/movies'].get()

    # Validate movies list
    assert_that(value, has_properties({
        'name': 'Movies',
        'description': None,
        'likes': 0,

        'allow_comments': True,
        'display_numbers': False,

        'updated_at': datetime(2015, 6, 22, 2, 25, tzinfo=tzutc()),

        'comment_count': 0,
        'item_count': 2,

        'privacy': 'private'
    }))


@responses.activate
def test_shows():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/shows',
        callback=authenticated_response('fixtures/users/me/lists/shows.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        value = Trakt['users/me/lists/shows'].get()

    # Validate shows list
    assert_that(value, has_properties({
        'name': 'Shows',
        'description': None,
        'likes': 0,

        'allow_comments': True,
        'display_numbers': False,

        'updated_at': datetime(2015, 6, 22, 2, 25, tzinfo=tzutc()),

        'comment_count': 0,
        'item_count': 3,

        'privacy': 'private'
    }))
