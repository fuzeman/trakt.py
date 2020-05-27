from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock
import datetime


def test_get():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            friends = Trakt['users/*/friends'].get('me')

            assert friends is not None

            friends = list(friends)

            assert friends[0].keys == [
                ('slug', 'sean')
            ]

            assert friends[1].keys == [
                ('slug', 'justin')
            ]

            assert isinstance(friends[0].friends_at, datetime.datetime)

            assert friends[0].name == 'Sean Rudford'

            assert friends[0].username == 'sean'
