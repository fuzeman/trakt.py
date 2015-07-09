from six.moves.urllib_parse import urlparse, parse_qsl
import os
import pytest
import six

if six.PY2:
    try:
        from six import cStringIO as BufferIO
    except ImportError:
        from six import StringIO as BufferIO
else:
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


def assert_url(url, expected_path, expected_query=None):
    __tracebackhide__ = True

    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query))

    if parsed.path != expected_path:
        pytest.fail("url.path is %r, expected %r" % (parsed.path, expected_path))

    if expected_query is not None and query != expected_query:
        pytest.fail('url.query is %r, expected %r' % (query, expected_query))
