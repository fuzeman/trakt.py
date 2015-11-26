from tests.core.helpers import read

from trakt import Trakt
import responses


@responses.activate
def test_shows_updates():
    responses.add(
        responses.GET, 'http://mock/shows/updates',
        body=read('fixtures/shows/updates.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    response = Trakt.http.get('/shows/updates')
    data = response.json()

    assert data[0]['show']['title'] == 'Breaking Bad'
    assert data[1]['show']['title'] == 'The Walking Dead'


@responses.activate
def test_show_progress_collection():
    responses.add(
        responses.GET, 'http://mock/shows/tt0944947/progress/collection',
        body=read('fixtures/shows/tt0944947/progress/collection.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    response = Trakt.http.get('/shows/tt0944947/progress/collection')
    data = response.json()

    assert data['aired'] == 10
    assert data['completed'] == 6
