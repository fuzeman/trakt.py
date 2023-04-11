# flake8: noqa: E241

from urllib.parse import urlparse, parse_qsl
import json
import math
import os
import pytest

from io import BytesIO as BufferIO

TESTS_PATH = os.path.abspath(os.path.dirname(__file__) + os.path.sep + '..')


def read(path, mode='rb'):
    if not os.path.isabs(path):
        path = os.path.join(TESTS_PATH, path)

    path = os.path.abspath(path)

    with open(path, mode) as fp:
        return BufferIO(fp.read())


def authenticated_response(path=None, data=None):
    def callback(request):
        h = request.headers

        if h.get('trakt-user-login') == 'mock' and h.get('trakt-user-token') == 'mock':
            return 200, {}, read(path) if path else data

        if h.get('Authorization') == 'Bearer mock':
            return 200, {}, read(path) if path else data

        return 401, {}, ''

    return callback


def pagination_response(path=None, authenticated=False):
    if not os.path.isabs(path):
        path = os.path.join(TESTS_PATH, path)

    path = os.path.abspath(path)

    # Parse file
    with open(path, 'r') as fp:
        collection = json.load(fp)

    # Construct request callback
    def callback(request):
        if authenticated and not is_authenticated(request.headers):
            return 401, {}, ''

        # Parse url
        url = urlparse(request.url)
        query = dict(parse_qsl(url.query))

        # Retrieve parameters
        page = int(query.get('page', 1))
        limit = int(query.get('limit', 10))

        # Retrieve page items
        start = (page - 1) * limit
        end = page * limit

        items = collection[start:end]

        if not items:
            return 404, {}, ''

        # Return page response
        page_count = int(math.ceil(
            float(len(collection)) / limit
        ))

        return (
            200, {
                'Content-Type':             'application/json',
                'X-Pagination-Page':        str(page),
                'X-Pagination-Limit':       str(limit),
                'X-Pagination-Page-Count':  str(page_count),
                'X-Pagination-Item-Count':  str(len(collection))
            },
            json.dumps(items)
        )

    return callback


def is_authenticated(headers):
    if headers.get('trakt-user-login') == 'mock' and headers.get('trakt-user-token') == 'mock':
        return True

    if headers.get('Authorization') == 'Bearer mock':
        return True

    return False


def assert_url(url, expected_path, expected_query=None):
    __tracebackhide__ = True

    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query))

    if parsed.path != expected_path:
        pytest.fail("url.path is %r, expected %r" % (parsed.path, expected_path))

    if expected_query is not None and query != expected_query:
        pytest.fail('url.query is %r, expected %r' % (query, expected_query))
