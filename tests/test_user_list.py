from tests.core.helpers import authenticated_response

from datetime import datetime
from dateutil.tz import tzutc
from trakt import Trakt
import responses


@responses.activate
def test_movies_get():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/movies',
        callback=authenticated_response('fixtures/users/me/lists/movies.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        movies_list = Trakt['users/me/lists/movies'].get()

    # Validate movies list
    assert movies_list.name == 'Movies'
    assert movies_list.description is None
    assert movies_list.likes == 0

    assert movies_list.allow_comments is True
    assert movies_list.display_numbers is False

    assert movies_list.updated_at == datetime(2015, 6, 22, 2, 25, tzinfo=tzutc())

    assert movies_list.comment_count == 0
    assert movies_list.item_count == 2

    assert movies_list.privacy == 'private'


@responses.activate
def test_shows_get():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/shows',
        callback=authenticated_response('fixtures/users/me/lists/shows.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        movies_list = Trakt['users/me/lists/shows'].get()

    # Validate movies list
    assert movies_list.name == 'Shows'
    assert movies_list.description is None
    assert movies_list.likes == 0

    assert movies_list.allow_comments is True
    assert movies_list.display_numbers is False

    assert movies_list.updated_at == datetime(2015, 6, 22, 2, 25, tzinfo=tzutc())

    assert movies_list.comment_count == 0
    assert movies_list.item_count == 3

    assert movies_list.privacy == 'private'


@responses.activate
def test_movies_items():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/movies/items',
        callback=authenticated_response('fixtures/users/me/lists/movies/items.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        items = Trakt['users/me/lists/movies'].items()

    # Validate movies items
    assert len(items) == 2

    # Mad Max: Fury Road (2015)
    assert items[0].title == 'Mad Max: Fury Road'
    assert items[0].year == 2015

    assert items[0].pk == ('imdb', 'tt1392190')
    assert items[0].keys == [
        ('imdb', 'tt1392190'),
        ('tmdb', '76341'),
        ('slug', 'mad-max-fury-road-2015'),
        ('trakt', '56360')
    ]

    assert items[1].listed_at == datetime(2015, 6, 24, 5, 50, 21, tzinfo=tzutc())

    # Maggie (2015)
    assert items[1].title == 'Maggie'
    assert items[1].year == 2015

    assert items[1].pk == ('imdb', 'tt1881002')
    assert items[1].keys == [
        ('imdb', 'tt1881002'),
        ('tmdb', '287424'),
        ('slug', 'maggie-1969'),
        ('trakt', '184504')
    ]

    assert items[1].listed_at == datetime(2015, 6, 24, 5, 50, 21, tzinfo=tzutc())


@responses.activate
def test_shows_items():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists/shows/items',
        callback=authenticated_response('fixtures/users/me/lists/shows/items.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        items = Trakt['users/me/lists/shows'].items()

    # Validate shows items
    assert len(items) == 3

    # Game of Thrones (2011)
    assert items[0].title == 'Game of Thrones'
    assert items[0].year == 2011

    assert items[0].pk == ('tvdb', '121361')
    assert items[0].keys == [
        ('tvdb', '121361'),
        ('tmdb', '1399'),
        ('imdb', 'tt0944947'),
        ('tvrage', '24493'),
        ('slug', 'game-of-thrones'),
        ('trakt', '1390')
    ]

    # Game of Thrones (2011) - S05
    assert items[1].pk == 5
    assert items[1].keys == [
        5,
        ('tmdb', '62090'),
        ('trakt', '3967')
    ]

    assert items[1].show.title == 'Game of Thrones'
    assert items[1].show.year == 2011

    # Game of Thrones (2011) - S05E04
    assert items[2].pk == (5, 4)
    assert items[2].keys == [
        (5, 4),
        ('tvdb', '5150183'),
        ('tmdb', '1045553'),
        ('imdb', 'tt3866838'),
        ('tvrage', '1065765456'),
        ('trakt', '1782362')
    ]

    assert items[2].show.title == 'Game of Thrones'
    assert items[2].show.year == 2011


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
