from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from datetime import datetime
from dateutil.tz import tzutc
from httmock import HTTMock


def test_create():
    with HTTMock(mock.list_create, mock.fixtures):
        with Trakt.configuration.auth('mock', 'mock'):
            movies = Trakt['users/me/lists'].create(name='Movies')

    # Validate movies list
    assert movies is not None

    assert movies.name == 'Movies'
    assert movies.description is None
    assert movies.likes == 0

    assert movies.allow_comments is True
    assert movies.display_numbers is False

    assert movies.updated_at == datetime(2015, 6, 22, 2, 25, tzinfo=tzutc())

    assert movies.comment_count == 0
    assert movies.item_count == 2

    assert movies.privacy == 'private'
