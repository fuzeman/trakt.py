from __future__ import absolute_import, division, print_function

from trakt.core.helpers import try_convert

from six.moves.urllib_parse import parse_qsl
import functools
import httmock
import itertools
import json
import math
import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
FIXTURES_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'fixtures'))


def authenticated(func):
    @functools.wraps(func)
    def wrapper(url, request, *args, **kwargs):
        if not is_authenticated(request):
            return httmock.httmock.response(403)

        return func(url, request, *args, **kwargs)

    return wrapper


def is_authenticated(request):
    # Ensure API Key has been provided
    if request.headers.get('trakt-api-key') not in ['mock-client_id', 'mock']:
        return False

    # OAuth
    if request.headers.get('Authorization') in ['Bearer mock-access_token', 'Bearer mock']:
        return True

    # xAuth
    return (
        request.headers.get('trakt-user-login') == 'mock' and request.headers.get('trakt-user-token') == 'mock'
    )


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
        return httmock.response(404, request=request)

    return httmock.response(
        200, content, {
            'Content-Type': 'application/json'
        },
        request=request
    )


def paginate(url, request, content_type='application/json'):
    parameters = dict(parse_qsl(url.query))

    page = try_convert(parameters.get('page'), int) or 1
    limit = try_convert(parameters.get('limit'), int) or 10

    # Retrieve items from fixture
    items = get_json(url.netloc, url.path, url.query)

    if items is None:
        return httmock.response(404, request=request)

    # Calculate page count and item offset
    offset = (page - 1) * limit
    page_count = int(math.ceil(float(len(items)) / limit))

    if request.method == 'HEAD':
        return httmock.response(
            200, '', {
                'Content-Type': content_type,

                'X-Pagination-Page': page,
                'X-Pagination-Limit': limit,
                'X-Pagination-Page-Count': page_count,
                'X-Pagination-Item-Count': len(items)
            },
            request=request
        )

    if request.method == 'GET':
        return httmock.response(
            200, json.dumps(items[offset:offset + limit]), {
                'Content-Type': content_type,

                'X-Pagination-Page': page,
                'X-Pagination-Limit': limit,
                'X-Pagination-Page-Count': page_count,
                'X-Pagination-Item-Count': len(items)
            },
            request=request
        )

    return httmock.response(404, request=request)


@httmock.urlmatch(netloc='api.trakt.tv')
def fixtures(url, request):
    return get_fixture(
        url.netloc, url.path,
        query=url.query,
        request=request
    )


@httmock.all_requests
def unknown(url, request):
    return httmock.response(501, request=request)


@httmock.urlmatch(netloc='api.trakt.tv', method='GET', path=r'/calendars/all/\w+/\d{4}-\d{2}-\d{2}(/\d{1,2})?')
def calendars_all_period(url, request):
    return fixtures(url, request)


@httmock.urlmatch(netloc='api.trakt.tv', method='GET', path=r'/calendars/my/\w+')
@authenticated
def calendars_my(url, request):
    return fixtures(url, request)


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path='/oauth/token')
def oauth_token(url, request):
    assert request.body

    # Validate request body
    data = json.loads(request.body)

    assert data.get('client_id') == 'mock-client_id'
    assert data.get('client_secret') == 'mock-client_secret'

    assert data.get('grant_type') in ['authorization_code', 'refresh_token']
    assert data.get('redirect_uri') == 'urn:ietf:wg:oauth:2.0:oob'

    if data['grant_type'] == 'authorization_code':
        assert data.get('code') == 'ABCD1234'
    else:
        assert data.get('refresh_token') == 'mock-refresh_token'

    # Return mock token
    return httmock.response(200, json.dumps({
        'access_token': 'mock-access_token',
        'token_type': 'bearer',
        'expires_in': 7200,
        'refresh_token': 'mock-refresh_token',
        'scope': 'public'
    }), {
        'Content-Type': 'application/json'
    })


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path='/oauth/device/code')
def oauth_device_code(url, request):
    assert request.body

    # Validate request body
    data = json.loads(request.body)

    assert data.get('client_id') == 'mock-client_id'

    # Return mock device code
    return httmock.response(200, json.dumps({
        'device_code': 'mock-device_code',
        'user_code': 'mock-user_code',
        'verification_url': 'https://trakt.tv/activate',
        'expires_in': 600,
        'interval': 5
    }), {
        'Content-Type': 'application/json'
    })


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path='/oauth/device/token')
def oauth_device_token(url, request):
    assert request.body

    # Validate request body
    data = json.loads(request.body)

    assert data.get('client_id') == 'mock-client_id'
    assert data.get('client_secret') == 'mock-client_secret'
    assert data.get('code') == 'mock-device_code'

    # Return mock token
    return httmock.response(200, json.dumps({
        'access_token': 'mock-access_token',
        'token_type': 'bearer',
        'expires_in': 7200,
        'refresh_token': 'mock-refresh_token',
        'scope': 'public'
    }), {
        'Content-Type': 'application/json'
    })


@httmock.urlmatch(netloc='api.trakt.tv', path=r'/users/likes')
@authenticated
def likes(url, request, content_type='application/json'):
    return paginate(url, request, content_type=content_type)


@httmock.urlmatch(netloc='api.trakt.tv', path=r'/users/likes')
def likes_invalid_content_type(url, request):
    return likes(url, request, content_type='text/plain')


@httmock.urlmatch(netloc='api.trakt.tv', path=r'/users/likes')
@authenticated
def likes_invalid_json(url, request):
    parameters = dict(parse_qsl(url.query))

    page = try_convert(parameters.get('page'), int) or 1

    # Return invalid response for page #2
    if request.method == 'GET' and page == 2:
        return httmock.response(
            200, '<invalid-json-response>', {
                'Content-Type': 'application/json'
            },
            request=request
        )

    # Return page
    return likes(url, request)


@httmock.urlmatch(netloc='api.trakt.tv', path=r'/users/likes')
@authenticated
def likes_request_failure(url, request):
    parameters = dict(parse_qsl(url.query))

    page = try_convert(parameters.get('page'), int) or 1

    # Return invalid response for page #2
    if request.method == 'GET' and page == 2:
        return httmock.response(400, request=request)

    # Return page
    return likes(url, request)


@httmock.urlmatch(netloc='api.trakt.tv', method='GET', path=r'/users/[\w-]+/lists')
@authenticated
def lists(url, request):
    return fixtures(url, request)


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path=r'/users/[\w-]+/lists')
@authenticated
def list_create(url, request):
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


@httmock.urlmatch(netloc='api.trakt.tv', method='GET', path=r'/users/[\w-]+/lists/[\w-]+')
@authenticated
def list_get(url, request):
    return fixtures(url, request)


@httmock.urlmatch(netloc='api.trakt.tv', method='DELETE', path=r'/users/[\w-]+/lists/[\w-]+')
@authenticated
def list_delete(url, request):
    return httmock.response(204, request=request)


@httmock.urlmatch(netloc='api.trakt.tv', method='PUT', path=r'/users/[\w-]+/lists/[\w-]+')
@authenticated
def list_update(url, request):
    return fixtures(url, request)


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path=r'/users/[\w-]+/lists/[\w-]+/like')
@authenticated
def list_like(url, request):
    return httmock.response(204, request=request)


@httmock.urlmatch(netloc='api.trakt.tv', method='DELETE', path=r'/users/[\w-]+/lists/[\w-]+/like')
@authenticated
def list_unlike(url, request):
    return httmock.response(204, request=request)


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path=r'/users/[\w-]+/lists/[\w-]+/items')
@authenticated
def list_item_add(url, request):
    return fixtures(url, request)


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path=r'/users/[\w-]+/lists/[\w-]+/items/remove')
@authenticated
def list_item_remove(url, request):
    return fixtures(url, request)


@authenticated
def scrobble(url, request, action):
    data = json.loads(request.body)
    assert data

    # Ensure provided identifier is correct
    assert data.get('movie', {}).get('ids', {}).get('tmdb') == 76341

    # Return response
    return httmock.response(
        200, {
            'id': 9832,
            'action': action,
            'progress': data.get('progress'),
            'sharing': {
                'facebook': False,
                'twitter': True,
                'tumblr': False
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


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path='/scrobble/start')
def scrobble_start(url, request):
    return scrobble(
        url, request,
        action='start'
    )


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path='/scrobble/pause')
def scrobble_pause(url, request):
    return scrobble(
        url, request,
        action='pause'
    )


@httmock.urlmatch(netloc='api.trakt.tv', method='POST', path='/scrobble/stop')
def scrobble_stop(url, request):
    return scrobble(
        url, request,
        action='stop'
    )


@httmock.urlmatch(netloc='api.trakt.tv', method='GET', path=r'/sync/\w+')
@authenticated
def sync_get(url, request):
    return fixtures(url, request)


@httmock.urlmatch(netloc='api.trakt.tv', path=r'/sync/history(/\w+)?')
@authenticated
def sync_history(url, request):
    return paginate(url, request)


@httmock.urlmatch(netloc='api.trakt.tv', method='DELETE', path=r'/sync/playback/\d+')
@authenticated
def sync_playback_delete(url, request):
    return httmock.response(204, request=request)


@httmock.urlmatch(netloc='api.trakt.tv', path=r'/sync/watchlist(/\w+)?')
@authenticated
def sync_watchlist(url, request):
    return paginate(url, request)
