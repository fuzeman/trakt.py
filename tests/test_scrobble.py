from tests.core.helpers import authenticated_response

from trakt import Trakt
import responses


@responses.activate
def test_start():
    responses.add_callback(
        responses.POST, 'http://mock/scrobble/start',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    with Trakt.configuration.auth('mock', 'mock'):
        result = Trakt['scrobble'].start(
            movie={'ids': {'tmdb': 76341}}
        )

    assert result is not None


@responses.activate
def test_pause():
    responses.add_callback(
        responses.POST, 'http://mock/scrobble/pause',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    with Trakt.configuration.auth('mock', 'mock'):
        result = Trakt['scrobble'].pause(
            movie={'ids': {'tmdb': 76341}}
        )

    assert result is not None


@responses.activate
def test_stop():
    responses.add_callback(
        responses.POST, 'http://mock/scrobble/stop',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    with Trakt.configuration.auth('mock', 'mock'):
        result = Trakt['scrobble'].stop(
            movie={'ids': {'tmdb': 76341}}
        )

    assert result is not None
