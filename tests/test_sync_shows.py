from tests.core.helpers import read

from datetime import datetime
from trakt import Trakt
import responses


@responses.activate
def test_playback():
    responses.add(
        responses.GET, 'http://mock/sync/playback/episodes',
        body=read('fixtures/sync/playback/episodes.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    playback = Trakt['sync/playback'].episodes()

    # Validate `Show`
    show = playback[('tvdb', '80348')]

    assert show.title == 'Chuck'
    assert show.year == 2007

    assert len(show.seasons) == 1
    assert len(show.seasons[1].episodes) == 2

    # Validate `Episode`
    episode = show.seasons[1].episodes[3]

    assert episode.paused_at == datetime(2015, 3, 9, 0, 10, 15)
    assert episode.progress == 4.99

    # Validate `Episode.to_dict()`
    data = episode.to_dict()

    assert data == {
        'progress': 4.99,
        'paused_at': '2015-03-09T00:10:15.000-00:00',

        'number': 3,
        'title': u'Chuck Versus the Tango',

        'ids': {
            'tvdb': '336271',
            'tmdb': '63434',
            'tvrage': '595113',
            'trakt': '74043'
        },

        'last_watched_at': None,
        'watched': 0,
        'plays': 0,

        'collected_at': None,
        'collected': 0,
    }


@responses.activate
def test_collection():
    responses.add(
        responses.GET, 'http://mock/sync/collection/shows',
        body=read('fixtures/sync/collection/shows.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    collection = Trakt['sync/collection'].shows()

    assert len(collection) == 4

    # Validate `Show`
    show = collection[('tvdb', '80348')]

    assert show.title == 'Chuck'
    assert show.year == 2007

    assert show.pk == ('tvdb', '80348')
    assert show.keys == [
        ('tvdb', '80348'),
        ('tmdb', '1404'),
        ('imdb', 'tt0934814'),
        ('tvrage', '15614'),
        ('slug', 'chuck'),
        ('trakt', '1395')
    ]

    assert len(show.seasons) == 1
    assert len(show.seasons[1].episodes) == 4

    # Validate `Episode`
    episode = show.seasons[1].episodes[2]

    assert episode.is_collected
    assert episode.collected_at == datetime(2013, 10, 11, 1, 59, 5)


@responses.activate
def test_ratings():
    responses.add(
        responses.GET, 'http://mock/sync/ratings/shows',
        body=read('fixtures/sync/ratings/shows.json'), status=200,
        content_type='application/json'
    )

    responses.add(
        responses.GET, 'http://mock/sync/ratings/episodes',
        body=read('fixtures/sync/ratings/episodes.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    ratings = {}

    Trakt['sync/ratings'].shows(ratings)
    Trakt['sync/ratings'].episodes(ratings)

    assert len(ratings) == 6

    # Validate `Show`
    show = ratings[('tvdb', '80348')]

    assert show.title == 'Chuck'
    assert show.year == 2007

    assert show.rating.value == 10
    assert show.rating.timestamp == datetime(2014, 10, 19, 23, 2, 23)

    # Validate `Episode`
    episode = show.seasons[1].episodes[1]

    assert episode.rating.value == 10
    assert episode.rating.timestamp == datetime(2014, 10, 19, 23, 2, 24)


@responses.activate
def test_watched():
    responses.add(
        responses.GET, 'http://mock/sync/watched/shows',
        body=read('fixtures/sync/watched/shows.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    watched = Trakt['sync/watched'].shows()

    assert len(watched) == 9

    # Validate `Show`
    show = watched[('tvdb', '80348')]

    assert show.title == 'Chuck'
    assert show.year == 2007

    assert len(show.seasons) == 1
    assert len(show.seasons[1].episodes) == 4

    # Validate `Episode`
    episode = show.seasons[1].episodes[2]

    assert episode.is_watched
    assert episode.last_watched_at == datetime(2015, 3, 10, 5, 21, 51)
    assert episode.plays == 9
