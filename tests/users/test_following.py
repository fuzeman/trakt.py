from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock
import datetime


def test_get():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            following = Trakt['users/*/following'].get('me')
            assert following is not None

            following = list(following)

            assert following[0].keys == [
                ('slug', 'sean')
            ]

            assert following[1].keys == [
                ('slug', 'justin')
            ]

            assert following[0].name == 'Sean Rudford'

            assert isinstance(following[0].followed_at, datetime.datetime)

            assert following[1].name == 'Justin Nemeth'
