from tests.core.helpers import authenticated_response

from datetime import datetime
from dateutil.tz import tzutc
from trakt import Trakt
import responses


@responses.activate
def test_create():
    responses.add_callback(
        responses.POST, 'http://mock/users/me/lists',
        callback=authenticated_response('fixtures/users/me/lists/movies.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        movies_list = Trakt['users/me/lists'].create(name="Movies")

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
def test_get():
    responses.add_callback(
        responses.GET, 'http://mock/users/me/lists',
        callback=authenticated_response('fixtures/users/me/lists.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        lists = Trakt['users/me/lists'].get()

        assert lists is not None

        # Resolve lists
        lists = list(lists)

    # Validate list container
    assert len(lists) == 1

    # Validate movies list
    movies_list = lists[0]

    assert movies_list.name == 'Movies'
    assert movies_list.description is None
    assert movies_list.likes == 0

    assert movies_list.allow_comments is True
    assert movies_list.display_numbers is False

    assert movies_list.updated_at == datetime(2015, 6, 22, 2, 25, tzinfo=tzutc())

    assert movies_list.comment_count == 0
    assert movies_list.item_count == 2

    assert movies_list.privacy == 'private'
