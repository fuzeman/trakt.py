from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock
import pytest


def test_likes():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            likes = Trakt['users'].likes()
            assert likes is not None

            likes = list(likes)

    assert len(likes) == 3

    assert likes[0].keys == [
        ('trakt', 1519)
    ]

    assert likes[1].keys == [
        ('trakt', '1238362'),
        ('slug', 'star-wars-machete')
    ]

    assert likes[2].keys == [
        ('trakt', '840781'),
        ('slug', 'star-wars-timeline')
    ]


def test_likes_invalid_response():
    with HTTMock(mock.fixtures, mock.unknown):
        likes = Trakt['users'].likes()

    assert likes is None


def test_likes_invalid_type():
    with HTTMock(mock.fixtures, mock.unknown):
        with pytest.raises(ValueError):
            likes = Trakt['users'].likes('invalid')
            assert likes is not None

            likes = list(likes)
