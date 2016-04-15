from tests.core.helpers import read

from six.moves.urllib.parse import parse_qsl, urlparse
from trakt import Trakt
from trakt.core.helpers import try_convert
import responses


@responses.activate
def test_iterator():
    def on_request(request):
        url = urlparse(request.url)
        parameters = dict(parse_qsl(url.query))

        page = try_convert(parameters.get('page'), int) or 1
        limit = try_convert(parameters.get('limit'), int)

        if limit is not None and limit != 2:
            # Invalid limit provided
            return 400, {}, ''

        return 200, {
            'X-Pagination-Limit':       '2',
            'X-Pagination-Item-Count':  '6',
            'X-Pagination-Page-Count':  '3'
        }, read('fixtures/users/me/lists_p%d.json' % page)

    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists',
        callback=on_request,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        lists = Trakt['users/me/lists'].get(pagination=True)

    # Resolve all pages
    items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 6

    assert [i.name for i in items] == [
        'Movies (1)',
        'Shows (1)',

        'Movies (2)',
        'Shows (2)',

        'Movies (3)',
        'Shows (3)'
    ]


@responses.activate
def test_invalid_content_type():
    def on_request(request):
        url = urlparse(request.url)
        parameters = dict(parse_qsl(url.query))

        page = try_convert(parameters.get('page'), int) or 1
        limit = try_convert(parameters.get('limit'), int)

        if limit is not None and limit != 2:
            # Invalid limit provided
            return 400, {}, ''

        return 200, {
            'X-Pagination-Limit':       '2',
            'X-Pagination-Item-Count':  '6',
            'X-Pagination-Page-Count':  '3'
        }, read('fixtures/users/me/lists_p%d.json' % page)

    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists',
        callback=on_request,
        content_type='text/plain'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        lists = Trakt['users/me/lists'].get(pagination=True)

    # Resolve all pages
    items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 0


@responses.activate
def test_invalid_json():
    def on_request(request):
        url = urlparse(request.url)
        parameters = dict(parse_qsl(url.query))

        page = try_convert(parameters.get('page'), int) or 1
        limit = try_convert(parameters.get('limit'), int)

        if limit is not None and limit != 2:
            # Invalid limit provided
            return 400, {}, ''

        if page == 2:
            return 200, {}, '<invalid-json-response>'

        return 200, {
            'X-Pagination-Limit':       '2',
            'X-Pagination-Item-Count':  '6',
            'X-Pagination-Page-Count':  '3'
        }, read('fixtures/users/me/lists_p%d.json' % page)

    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists',
        callback=on_request,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        lists = Trakt['users/me/lists'].get(pagination=True)

    # Resolve all pages
    items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 2


@responses.activate
def test_request_failure():
    def on_request(request):
        url = urlparse(request.url)
        parameters = dict(parse_qsl(url.query))

        page = try_convert(parameters.get('page'), int) or 1
        limit = try_convert(parameters.get('limit'), int)

        if limit is not None and limit != 2:
            # Invalid limit provided
            return 400, {}, ''

        if page == 2:
            return 400, {}, ''

        return 200, {
            'X-Pagination-Limit':       '2',
            'X-Pagination-Item-Count':  '6',
            'X-Pagination-Page-Count':  '3'
        }, read('fixtures/users/me/lists_p%d.json' % page)

    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists',
        callback=on_request,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        lists = Trakt['users/me/lists'].get(pagination=True)

    # Resolve all pages
    items = list(lists)

    # Ensure items were returned correctly
    assert len(items) == 2
