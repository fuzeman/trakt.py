from tests.core.helpers import authenticated_response

from trakt import Trakt
import responses


@responses.activate
def test_list_add():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/movies',
        callback=authenticated_response('fixtures/users/me/lists/movies.json'),
        content_type='application/json'
    )

    responses.add_callback(
        responses.POST, 'http://mock/users/me/lists/123456/items',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        movies_list = Trakt['users/me/lists/movies'].get()

        result = movies_list.add({
            'shows': [
                {'ids': {'tvdb': 121361}}
            ]
        })

    assert result is not None


@responses.activate
def test_list_delete():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/movies',
        callback=authenticated_response('fixtures/users/me/lists/movies.json'),
        content_type='application/json'
    )

    responses.add_callback(
        responses.DELETE, 'http://mock/users/me/lists/123456',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        movies_list = Trakt['users/me/lists/movies'].get()

        success = movies_list.delete()

    assert success is True


@responses.activate
def test_list_update():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/movies',
        callback=authenticated_response('fixtures/users/me/lists/movies.json'),
        content_type='application/json'
    )

    responses.add_callback(
        responses.PUT, 'http://mock/users/me/lists/123456',
        callback=authenticated_response('fixtures/users/me/lists/shows.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        movies_list = Trakt['users/me/lists/movies'].get()

        result = movies_list.update(
            name="Shows (2)"
        )

    assert result is not None


@responses.activate
def test_list_remove():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/movies',
        callback=authenticated_response('fixtures/users/me/lists/movies.json'),
        content_type='application/json'
    )

    responses.add_callback(
        responses.POST, 'http://mock/users/me/lists/123456/items/remove',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        movies_list = Trakt['users/me/lists/movies'].get()

        result = movies_list.remove({
            'shows': [
                {'ids': {'tvdb': 121361}}
            ]
        })

    assert result is not None


@responses.activate
def test_list_like():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/movies',
        callback=authenticated_response('fixtures/users/me/lists/movies.json'),
        content_type='application/json'
    )

    responses.add_callback(
        responses.POST, 'http://mock/users/me/lists/123456/like',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        movies_list = Trakt['users/me/lists/movies'].get()

        success = movies_list.like()

    assert success is True


@responses.activate
def test_list_unlike():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/movies',
        callback=authenticated_response('fixtures/users/me/lists/movies.json'),
        content_type='application/json'
    )

    responses.add_callback(
        responses.DELETE, 'http://mock/users/me/lists/123456/like',
        callback=authenticated_response(data='{"mock": "mock"}'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        movies_list = Trakt['users/me/lists/movies'].get()

        success = movies_list.unlike()

    assert success is True