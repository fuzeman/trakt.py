from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock


def test_delete():
    with HTTMock(mock.list_get, mock.list_delete):
        with Trakt.configuration.auth('mock', 'mock'):
            shows = Trakt['users/sean/lists/star-wars-in-machete-order'].get()
            assert shows is not None

            success = shows.delete()

    assert success is True


def test_update():
    with HTTMock(mock.list_get, mock.list_update):
        with Trakt.configuration.auth('mock', 'mock'):
            shows = Trakt['users/sean/lists/star-wars-in-machete-order'].get()
            assert shows is not None

            result = shows.update(
                name='Shows (2)'
            )

    assert result is not None


def test_like():
    with HTTMock(mock.list_get, mock.list_like):
        with Trakt.configuration.auth('mock', 'mock'):
            shows = Trakt['users/sean/lists/star-wars-in-machete-order'].get()
            assert shows is not None

            success = shows.like()

    assert success is True


def test_unlike():
    with HTTMock(mock.list_get, mock.list_unlike):
        with Trakt.configuration.auth('mock', 'mock'):
            shows = Trakt['users/sean/lists/star-wars-in-machete-order'].get()
            assert shows is not None

            success = shows.unlike()

    assert success is True


def test_item_add():
    with HTTMock(mock.list_get, mock.list_item_add):
        with Trakt.configuration.auth('mock', 'mock'):
            shows = Trakt['users/sean/lists/star-wars-in-machete-order'].get()
            assert shows is not None

            result = shows.add({
                'shows': [
                    {'ids': {'tvdb': 121361}}
                ]
            })

    assert result is not None


def test_item_remove():
    with HTTMock(mock.list_get, mock.list_item_remove):
        with Trakt.configuration.auth('mock', 'mock'):
            shows = Trakt['users/sean/lists/star-wars-in-machete-order'].get()
            assert shows is not None

            result = shows.remove({
                'shows': [
                    {'ids': {'tvdb': 121361}}
                ]
            })

    assert result is not None
