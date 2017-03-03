from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from datetime import datetime
from dateutil.tz import tzutc
from httmock import HTTMock


def test_basic():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            lists = Trakt['users/me/lists'].get()

            assert lists is not None

            # Resolve lists
            lists = list(lists)

    # Validate list container
    assert len(lists) == 37

    # Validate movies list
    movies = lists[0]

    assert movies.name == 'Movies'
    assert movies.description is None
    assert movies.likes == 0

    assert movies.allow_comments is True
    assert movies.display_numbers is False

    assert movies.updated_at == datetime(2015, 6, 22, 2, 25, tzinfo=tzutc())

    assert movies.comment_count == 0
    assert movies.item_count == 2

    assert movies.privacy == 'private'
