

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock
import datetime


def test_get():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['users/*/watchlist'].get('me')

            assert items is not None

            items = list(items)

            assert len(items) == 2

            assert items[0] is not None

            assert isinstance(items[0].listed_at, datetime.datetime)

            assert items[0].title == 'TRON: Legacy'
