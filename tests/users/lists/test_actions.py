from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock


def test_delete():
    with HTTMock(mock.list_delete, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            success = Trakt['users/sean/lists/star-wars-in-machete-order'].delete()

    assert success is True


def test_update_data():
    with HTTMock(mock.list_update, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['users/sean/lists/star-wars-in-machete-order'].update(
                name='Shows (2)',
                return_type='data'
            )

    assert result is not None


def test_update_object():
    with HTTMock(mock.list_update, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['users/sean/lists/star-wars-in-machete-order'].update(
                name='Shows (2)'
            )

    assert result is not None


def test_like():
    with HTTMock(mock.list_like, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            success = Trakt['users/sean/lists/star-wars-in-machete-order'].like()

    assert success is True


def test_unlike():
    with HTTMock(mock.list_unlike, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            success = Trakt['users/sean/lists/star-wars-in-machete-order'].unlike()

    assert success is True


def test_item_add():
    with HTTMock(mock.list_item_add, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['users/sean/lists/star-wars-in-machete-order'].add({
                'shows': [
                    {'ids': {'tvdb': 121361}}
                ]
            })

    assert result is not None


def test_item_remove():
    with HTTMock(mock.list_item_remove, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['users/sean/lists/star-wars-in-machete-order'].remove({
                'shows': [
                    {'ids': {'tvdb': 121361}}
                ]
            })

    assert result is not None
