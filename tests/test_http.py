from tests.core import mock
from trakt import Trakt

from httmock import HTTMock


def test_shows_updates():
    with HTTMock(mock.fixtures, mock.unknown):
        response = Trakt.http.get('/shows/updates')

    items = response.json()

    assert [item['show']['title'] for item in items] == [
        'The Pop Game',
        'The Pop Game',
        'Abandoned Engineering'
    ]


def test_show_progress_collection():
    # TODO Add missing fixture
    with HTTMock(mock.fixtures, mock.unknown):
        response = Trakt.http.get('/shows/tt0944947/progress/collection')

    data = response.json()

    assert data['aired'] == 10
    assert data['completed'] == 6
