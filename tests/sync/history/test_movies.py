# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt

from hamcrest import *
from httmock import HTTMock
from six.moves import xrange


def test_basic():
    with HTTMock(mock.sync_history, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            history = Trakt['sync/history'].movies(pagination=True, per_page=5)

            # Ensure collection is valid
            assert_that(history, not_none())

            # Resolve all pages
            items = list(history)

    # Ensure all items have been returned
    assert_that(items, has_length(25))

    # Verify item identifiers
    assert_that(
        [item.id for item in items],
        equal_to(list(xrange(1, 26)))
    )
