from tests.core.helpers import pagination_response

from hamcrest import *
from six.moves import xrange
from trakt import Trakt
import responses


@responses.activate
def test_basic():
    responses.add_callback(
        responses.GET, 'http://mock/sync/history',
        callback=pagination_response(
            'fixtures/sync/history.json',
            authenticated=True
        )
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        history = Trakt['sync/history'].get(pagination=True, per_page=5)

    # Ensure collection is valid
    assert_that(history, not_none())

    # Resolve all pages
    items = list(history)

    # Ensure all items have been returned
    assert_that(items, has_length(3))

    # Verify item identifiers
    assert_that(
        [item.id for item in items],
        equal_to(list(xrange(1, 4)))
    )
