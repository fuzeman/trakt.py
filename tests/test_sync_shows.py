from tests.core.helpers import authenticated_response

from datetime import datetime
from trakt import Trakt
import responses


@responses.activate
def test_playback():
    responses.add_callback(
        responses.GET, 'http://mock/sync/playback/episodes',
        callback=authenticated_response('fixtures/sync/playback/episodes.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        playback = Trakt['sync/playback'].episodes()

    assert playback is not None

    # Validate `Show`
    show = playback[('tvdb', '80348')]

    assert show.title == 'Chuck'
    assert show.year == 2007

    assert len(show.seasons) == 1

    # Validate `Season`
    season = show.seasons[1]

    assert season.show == show

    assert len(season.episodes) == 2

    # Validate `Episode`
    episode = season.episodes[3]

    assert episode.show == show
    assert episode.season == season

    assert episode.paused_at == datetime(2015, 3, 9, 0, 10, 15)
    assert episode.progress == 4.99

    # Validate `Episode.to_dict()`
    assert episode.to_dict() == {
        'progress': 4.99,
        'paused_at': '2015-03-09T00:10:15.000-00:00',

        'number': 3,
        'title': 'Chuck Versus the Tango',

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
        'collected': 0
    }


@responses.activate
def test_collection():
    responses.add_callback(
        responses.GET, 'http://mock/sync/collection/shows',
        callback=authenticated_response('fixtures/sync/collection/shows.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        collection = Trakt['sync/collection'].shows()

    assert collection is not None
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

    # Validate `Season`
    season = show.seasons[1]

    assert season.show == show

    assert len(season.episodes) == 4

    # Validate `Episode`
    episode = season.episodes[2]

    assert episode.show == show
    assert episode.season == season

    assert episode.is_collected
    assert episode.collected_at == datetime(2013, 10, 11, 1, 59, 5)


@responses.activate
def test_ratings():
    responses.add_callback(
        responses.GET, 'http://mock/sync/ratings/shows',
        callback=authenticated_response('fixtures/sync/ratings/shows.json'),
        content_type='application/json'
    )

    responses.add_callback(
        responses.GET, 'http://mock/sync/ratings/seasons',
        callback=authenticated_response('fixtures/sync/ratings/seasons.json'),
        content_type='application/json'
    )

    responses.add_callback(
        responses.GET, 'http://mock/sync/ratings/episodes',
        callback=authenticated_response('fixtures/sync/ratings/episodes.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    ratings = {}

    with Trakt.configuration.auth('mock', 'mock'):
        Trakt['sync/ratings'].shows(ratings)
        Trakt['sync/ratings'].seasons(ratings)
        Trakt['sync/ratings'].episodes(ratings)

    assert len(ratings) == 6

    # Validate `Show`
    show = ratings[('tvdb', '80348')]

    assert show.title == 'Chuck'
    assert show.year == 2007

    assert show.rating.value == 10
    assert show.rating.timestamp == datetime(2014, 10, 19, 23, 2, 23)

    # Validate `Season`
    season = show.seasons[1]

    assert season.show == show

    assert season.keys == [
        1,
        ('tvdb', '27985'),
        ('tmdb', '3650'),
        ('trakt', '3993')
    ]

    assert season.rating.value == 10
    assert season.rating.timestamp == datetime(2015, 3, 11, 23, 29, 35)

    # Validate `Season.to_dict()`
    assert season.to_dict() == {
        'number': 1,
        'episodes': [
            {
                'progress': None,
                'paused_at': None,

                'number': 1,
                'title': 'Chuck Versus the Intersect',

                'ids': {
                    'tvdb': '332179',
                    'tmdb': '63425',
                    'tvrage': '579282',
                    'trakt': '74041'
                },

                'last_watched_at': None,
                'watched': 0,
                'plays': 0,

                'collected_at': None,
                'collected': 0,

                'rating': 10,
                'rated_at': '2014-10-19T23:02:24.000-00:00'
            }
        ],
        'ids': {
            'tvdb': '27985',
            'tmdb': '3650',
            'trakt': '3993'
        },

        'rating': 10,
        'rated_at': '2015-03-11T23:29:35.000-00:00'
    }

    # Validate `Episode`
    episode = season.episodes[1]

    assert episode.show == show
    assert episode.season == season

    assert episode.rating.value == 10
    assert episode.rating.timestamp == datetime(2014, 10, 19, 23, 2, 24)


@responses.activate
def test_watched():
    responses.add_callback(
        responses.GET, 'http://mock/sync/watched/shows',
        callback=authenticated_response('fixtures/sync/watched/shows.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        watched = Trakt['sync/watched'].shows()

    assert watched is not None
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
