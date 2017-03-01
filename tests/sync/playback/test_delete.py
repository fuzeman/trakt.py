# flake8: noqa: E221

from tests.core.helpers import authenticated_response
from trakt import Trakt
from trakt.objects import Movie, Show, Episode

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
import responses


@responses.activate
def test_basic():
    responses.add_callback(
        responses.GET, 'http://mock/sync/playback',
        callback=authenticated_response('fixtures/sync/playback/delete.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        collection = Trakt['sync/playback'].get()

    # Ensure collection is valid
    assert_that(collection, not_none())
    
    # Batman Begins (2005)
    assert_that(collection[('imdb', 'tt0372784')], has_properties({
        'id': 13
    }))
    
    # Breaking Bad (2008)
    assert_that(collection[('tvdb', '81189')], has_properties({

        # Seasons
        'seasons': all_of(
            has_length(1),

            # Seasons
            has_entry(0, has_properties({
                'episodes': all_of(
                    has_length(1),

                    # Episodes
                    has_entry(1, has_properties({
                        'id': 37
                    }))
                )
            }))
        ),
    }))

    # Batman Begins (2005)
    responses.add_callback(
        responses.DELETE, 'http://mock/sync/playback/13',  # 13 = collection[('imdb', 'tt0372784')].id
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )
    
    # Breaking Bad (2008) - S00E01 - Good Cop Bad Cop
    responses.add_callback(
        responses.DELETE, 'http://mock/sync/playback/37',  # 37 = collection[('tvdb', '81189')].seasons[0].episodes[1].id
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    with Trakt.configuration.auth('mock', 'mock'):
        success_movie   = Trakt['sync/playback'].delete(13)
        success_episode = Trakt['sync/playback'].delete(37)

    assert success_movie is True
    assert success_episode is True
