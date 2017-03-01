from tests.core.helpers import authenticated_response
from trakt import Trakt

import responses


@responses.activate
def test_add():
    responses.add_callback(
        responses.POST, 'http://mock/users/me/lists/shows/items',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        result = Trakt['users/me/lists/shows'].add({
            'shows': [
                {'ids': {'tvdb': 121361}}
            ]
        })

    assert result is not None


@responses.activate
def test_delete():
    responses.add_callback(
        responses.DELETE, 'http://mock/users/me/lists/shows',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        success = Trakt['users/me/lists/shows'].delete()

    assert success is True


@responses.activate
def test_update_data():
    responses.add_callback(
        responses.PUT, 'http://mock/users/me/lists/shows',
        callback=authenticated_response('fixtures/users/me/lists/shows.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        result = Trakt['users/me/lists/shows'].update(
            name="Shows (2)",
            return_type='data'
        )

    assert result is not None


@responses.activate
def test_update_object():
    responses.add_callback(
        responses.PUT, 'http://mock/users/me/lists/shows',
        callback=authenticated_response('fixtures/users/me/lists/shows.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        result = Trakt['users/me/lists/shows'].update(
            name="Shows (2)"
        )

    assert result is not None


@responses.activate
def test_remove():
    responses.add_callback(
        responses.POST, 'http://mock/users/me/lists/shows/items/remove',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        result = Trakt['users/me/lists/shows'].remove({
            'shows': [
                {'ids': {'tvdb': 121361}}
            ]
        })

    assert result is not None


@responses.activate
def test_like():
    responses.add_callback(
        responses.POST, 'http://mock/users/me/lists/shows/like',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        success = Trakt['users/me/lists/shows'].like()

    assert success is True


@responses.activate
def test_unlike():
    responses.add_callback(
        responses.DELETE, 'http://mock/users/me/lists/shows/like',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        success = Trakt['users/me/lists/shows'].unlike()

    assert success is True
