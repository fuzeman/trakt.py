from tests.core.helpers import read

from trakt import Trakt
import responses


@responses.activate
def test_movie():
    responses.add(
        responses.GET, 'http://mock/movies/tron-legacy-2010',
        body=read('fixtures/movies/tron-legacy-2010.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    movie = Trakt['movies'].get('tron-legacy-2010')

    assert movie.title == 'TRON: Legacy'
    assert movie.year == 2010

    assert movie.pk == ('imdb', 'tt1104001')

    assert movie.keys == [
        ('imdb', 'tt1104001'),
        ('tmdb', '20526'),
        ('slug', 'tron-legacy-2010'),
        ('trakt', '12601')
    ]


@responses.activate
def test_show():
    responses.add(
        responses.GET, 'http://mock/shows/1390',
        body=read('fixtures/shows/1390.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    show = Trakt['shows'].get(1390)

    assert show.title == 'Game of Thrones'
    assert show.year == 2011

    assert show.pk == ('tvdb', '121361')
    assert show.keys == [
        ('tvdb', '121361'),
        ('tmdb', '1399'),
        ('imdb', 'tt0944947'),
        ('tvrage', '24493'),
        ('slug', 'game-of-thrones'),
        ('trakt', '1390')
    ]


@responses.activate
def test_seasons():
    responses.add(
        responses.GET, 'http://mock/shows/tt0944947/seasons',
        body=read('fixtures/shows/tt0944947/seasons.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    seasons = Trakt['shows'].seasons('tt0944947')

    assert len(seasons) == 6

    assert seasons[0].pk == 0
    assert seasons[0].keys == [
        0,
        ('tvdb', '137481'),
        ('tmdb', '3627'),
        ('trakt', '3962')
    ]

    assert seasons[5].pk == 5
    assert seasons[5].keys == [
        5,
        ('tmdb', '62090'),
        ('trakt', '3967')
    ]


@responses.activate
def test_season():
    responses.add(
        responses.GET, 'http://mock/shows/game-of-thrones/seasons/1',
        body=read('fixtures/shows/game-of-thrones/seasons/1.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    episodes = Trakt['shows'].season('game-of-thrones', 1)

    assert len(episodes) == 10

    assert episodes[0].title == 'Winter Is Coming'
    assert episodes[0].pk == (1, 1)
    assert episodes[0].keys == [
        (1, 1),
        ('tvdb', '3254641'),
        ('tmdb', '63056'),
        ('imdb', 'tt1480055'),
        ('tvrage', '1065008299'),
        ('trakt', '73640')
    ]

    assert episodes[9].title == 'Fire and Blood'
    assert episodes[9].pk == (1, 10)
    assert episodes[9].keys == [
        (1, 10),
        ('tvdb', '4063491'),
        ('tmdb', '63065'),
        ('imdb', 'tt1851397'),
        ('tvrage', '1065039307'),
        ('trakt', '73649')
    ]


@responses.activate
def test_episode_basic():
    responses.add(
        responses.GET, 'http://mock/shows/game-of-thrones/seasons/1/episodes/1',
        body=read('fixtures/shows/game-of-thrones/seasons/1/episodes/1.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    episode = Trakt['shows'].episode('game-of-thrones', 1, 1)

    assert episode.title == 'Winter Is Coming'
    assert episode.pk == (1, 1)
    assert episode.keys == [
        (1, 1),
        ('tvdb', '3254641'),
        ('tmdb', '63056'),
        ('imdb', 'tt1480055'),
        ('tvrage', '1065008299'),
        ('trakt', '73640')
    ]


@responses.activate
def test_episode_proxy():
    responses.add(
        responses.GET, 'http://mock/shows/game-of-thrones/seasons/1/episodes/1',
        body=read('fixtures/shows/game-of-thrones/seasons/1/episodes/1.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    episode = Trakt['shows/game-of-thrones'].episode(1, 1)

    assert episode.title == 'Winter Is Coming'
    assert episode.pk == (1, 1)
    assert episode.keys == [
        (1, 1),
        ('tvdb', '3254641'),
        ('tmdb', '63056'),
        ('imdb', 'tt1480055'),
        ('tvrage', '1065008299'),
        ('trakt', '73640')
    ]
