from trakt.core.helpers import try_convert

from httmock import all_requests, response, urlmatch
from urlparse import parse_qsl
import itertools
import json
import math
import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
FIXTURES_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'fixtures'))


def get_content(netloc, path, query=None):
    components = path.strip('/').split('/') + list(itertools.chain.from_iterable([
        ('#' + key, value) for key, value in sorted(parse_qsl(query or ''))
    ]))
    path = None

    # Search for matching fixture
    current = os.path.join(FIXTURES_DIR, netloc)

    for component in components:
        current = os.path.join(current, component)

        if os.path.exists(current + '.json'):
            path = current + '.json'

        if not os.path.exists(current):
            break

    if not path:
        return None

    # Read fixture content
    with open(path, 'r') as fp:
        return fp.read()


def get_json(netloc, path, query=None):
    content = get_content(netloc, path, query)

    if content is None:
        return None

    return json.loads(content)


def get_fixture(netloc, path, query=None, request=None):
    content = get_content(netloc, path, query)

    if content is None:
        return response(404, request=request)

    return response(
        200, content, {
            'Content-Type': 'application/json'
        },
        request=request
    )


@urlmatch(netloc='api.trakt.tv')
def fixtures(url, request):
    return get_fixture(
        url.netloc, url.path,
        query=url.query,
        request=request
    )


@all_requests
def unknown(url, request):
    return response(501, request=request)


@urlmatch(netloc='api.trakt.tv', method='GET', path=r'/users/[\w-]+/lists')
def lists(url, request, content_type='application/json'):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Retrieve parameters
    parameters = dict(parse_qsl(url.query))

    page = try_convert(parameters.get('page'), int) or 1
    limit = try_convert(parameters.get('limit'), int) or 10

    # Retrieve items from fixture
    items = get_json(url.netloc, url.path, url.query)

    if items is None:
        return response(404, request=request)

    # Calculate page count and item offset
    offset = (page - 1) * limit
    page_count = int(math.ceil(float(len(items)) / limit))

    return response(
        200, json.dumps(items[offset:offset + limit]), {
            'Content-Type': content_type,

            'X-Pagination-Page': page,
            'X-Pagination-Limit': limit,
            'X-Pagination-Page-Count': page_count,
            'X-Pagination-Item-Count': len(items)
        },
        request=request
    )


@urlmatch(netloc='api.trakt.tv', method='GET', path=r'/users/[\w-]+/lists')
def lists_invalid_content_type(url, request):
    return lists(url, request, content_type='text/plain')


@urlmatch(netloc='api.trakt.tv', method='GET', path=r'/users/[\w-]+/lists')
def lists_invalid_json(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Retrieve parameters
    parameters = dict(parse_qsl(url.query))

    page = try_convert(parameters.get('page'), int) or 1

    # Return invalid response for page #2
    if page == 2:
        return response(
            200, '<invalid-json-response>', {
                'Content-Type': 'application/json'
            },
            request=request
        )

    # Return page
    return lists(url, request)


@urlmatch(netloc='api.trakt.tv', method='GET', path=r'/users/[\w-]+/lists')
def lists_request_failure(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Retrieve parameters
    parameters = dict(parse_qsl(url.query))

    page = try_convert(parameters.get('page'), int) or 1

    # Return invalid response for page #2
    if page == 2:
        return response(400, request=request)

    # Return page
    return lists(url, request)


@urlmatch(netloc='api.trakt.tv', method='POST', path=r'/users/[\w-]+/lists')
def list_create(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Retrieve list attributes
    data = json.loads(request.body)

    assert data
    assert data.get('name')

    # Generate slug from list name
    slug = data['name'].lower().replace(' ', '-')

    # Return fixture
    return get_fixture(
        url.netloc, '%s/%s' % (url.path, slug),
        query=url.query,
        request=request
    )


@urlmatch(netloc='api.trakt.tv', method='GET', path=r'/users/[\w-]+/lists/[\w-]+')
def list_get(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Return fixture
    return fixtures(url, request)


@urlmatch(netloc='api.trakt.tv', method='DELETE', path=r'/users/[\w-]+/lists/[\w-]+')
def list_delete(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Return response
    return response(204, request=request)


@urlmatch(netloc='api.trakt.tv', method='PUT', path=r'/users/[\w-]+/lists/[\w-]+')
def list_update(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Return fixture
    return fixtures(url, request)


@urlmatch(netloc='api.trakt.tv', method='POST', path=r'/users/[\w-]+/lists/[\w-]+/like')
def list_like(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Return response
    return response(204, request=request)


@urlmatch(netloc='api.trakt.tv', method='DELETE', path=r'/users/[\w-]+/lists/[\w-]+/like')
def list_unlike(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Return response
    return response(204, request=request)


@urlmatch(netloc='api.trakt.tv', method='POST', path=r'/users/[\w-]+/lists/[\w-]+/items')
def list_item_add(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Return fixture
    return fixtures(url, request)


@urlmatch(netloc='api.trakt.tv', method='POST', path=r'/users/[\w-]+/lists/[\w-]+/items/remove')
def list_item_remove(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Return fixture
    return fixtures(url, request)


def scrobble(url, request, action):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Ensure body exists
    data = json.loads(request.body)
    assert data

    # Ensure provided identifier is correct
    assert data.get('movie', {}).get('ids', {}).get('tmdb') == 76341

    # Return response
    return response(
        200, {
            'id': 9832,
            'action': action,
            'progress': data.get('progress'),
            'sharing': {
                "facebook": False,
                "twitter": True,
                "tumblr": False
            },
            'movie': {
                'title': 'Mad Max: Fury Road',
                'year': 2015,
                'ids': {
                    'trakt': 56360,
                    'slug': 'mad-max-fury-road-2015',
                    'imdb': 'tt1392190',
                    'tmdb': 76341
                }
            }
        }, {
            'Content-Type': 'application/json'
        },
        request=request
    )


@urlmatch(netloc='api.trakt.tv', method='POST', path='/scrobble/start')
def scrobble_start(url, request):
    return scrobble(
        url, request,
        action='start'
    )


@urlmatch(netloc='api.trakt.tv', method='POST', path='/scrobble/pause')
def scrobble_pause(url, request):
    return scrobble(
        url, request,
        action='pause'
    )


@urlmatch(netloc='api.trakt.tv', method='POST', path='/scrobble/stop')
def scrobble_stop(url, request):
    return scrobble(
        url, request,
        action='stop'
    )


@urlmatch(netloc='api.trakt.tv', method='GET', path='/sync/\w+')
def sync_get(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Return fixture
    return fixtures(url, request)


@urlmatch(netloc='api.trakt.tv', method='DELETE', path='/sync/playback/\d+')
def sync_playback_delete(url, request):
    # Ensure credentials were provided
    assert request.headers.get('trakt-user-login') == 'mock'
    assert request.headers.get('trakt-user-token') == 'mock'

    # Return fixture
    return response(204, request=request)
