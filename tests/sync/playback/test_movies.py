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
        responses.GET, 'http://mock/sync/playback/movies',
        callback=authenticated_response('fixtures/sync/playback/movies.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        collection = Trakt['sync/playback'].movies()

    # Ensure collection is valid
    assert_that(collection, not_none())

    # TRON: Legacy (2010)
    assert_that(collection[('imdb', 'tt1104001')], has_properties({
        'pk': ('imdb', 'tt1104001'),
        'title': 'TRON: Legacy',
        'year': 2010,

        'progress': 64.0,

        # Timestamps
        'paused_at': datetime(2015, 2, 9, 5, 56, 58, tzinfo=tzutc()),

        # Keys
        'keys': [
            ('imdb',  'tt1104001'),
            ('tmdb',  '20526'),
            ('slug',  'tron-legacy-2010'),
            ('trakt', '12601')
        ]
    }))

    # 100 Bloody Acres (2012)
    assert_that(collection[('imdb', 'tt2290065')], has_properties({
        'pk': ('imdb', 'tt2290065'),
        'title': '100 Bloody Acres',
        'year': 2012,

        'progress': 0.0,

        # Timestamps
        'paused_at': datetime(2015, 1, 10, 6, 44, 9, tzinfo=tzutc()),

        # Keys
        'keys': [
            ('imdb', 'tt2290065'),
            ('tmdb', '126757'),
            ('slug', '100-bloody-acres-2012'),
            ('trakt', '86920')
        ]
    }))
