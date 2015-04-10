import os
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


def authenticated_response(path):
    def callback(request):
        h = request.headers

        if h.get('trakt-user-login') == 'mock' and h.get('trakt-user-token') == 'mock':
            return 200, {}, read(path)

        if h.get('Authorization') == 'Bearer mock':
            return 200, {}, read(path)

        return 401, {}, ''

    return callback