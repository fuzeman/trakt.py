from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock


def test_movie():
    with HTTMock(mock.fixtures, mock.unknown):
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


def test_movie_not_found():
    with HTTMock(mock.fixtures, mock.unknown):
        movie = Trakt['movies'].get('not-found-4040')

    assert movie is None


def test_show():
    with HTTMock(mock.fixtures, mock.unknown):
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


def test_show_not_found():
    with HTTMock(mock.fixtures, mock.unknown):
        show = Trakt['shows'].get(0)

    assert show is None


def test_seasons():
    with HTTMock(mock.fixtures, mock.unknown):
        seasons = Trakt['shows'].seasons('tt0944947')

    assert len(seasons) == 7

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
        ('tvdb', '607490'),
        ('tmdb', '62090'),
        ('trakt', '3967')
    ]


def test_seasons_extended():
    with HTTMock(mock.fixtures, mock.unknown):
        seasons = Trakt['shows'].seasons('tt0944947', extended='episodes')

    assert len(seasons) == 7

    # Specials
    assert seasons[0].pk == 0
    assert seasons[0].keys == [
        0,
        ('tvdb', '137481'),
        ('tmdb', '3627'),
        ('trakt', '3962')
    ]

    assert len(seasons[0].episodes) == 23

    assert seasons[0].episodes[5].pk == (0, 5)
    assert seasons[0].episodes[5].title == '2011 Comic Con Panel'

    assert seasons[0].episodes[13].pk == (0, 13)
    assert seasons[0].episodes[13].title == 'World Premiere'

    # Season 5
    assert seasons[5].pk == 5
    assert seasons[5].keys == [
        5,
        ('tvdb', '607490'),
        ('tmdb', '62090'),
        ('trakt', '3967')
    ]

    assert len(seasons[5].episodes) == 10

    assert seasons[5].episodes[7].pk == (5, 7)
    assert seasons[5].episodes[7].title == 'The Gift'

    assert seasons[5].episodes[9].pk == (5, 9)
    assert seasons[5].episodes[9].title == 'The Dance of Dragons'


def test_season():
    with HTTMock(mock.fixtures, mock.unknown):
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


def test_season_not_found():
    with HTTMock(mock.fixtures, mock.unknown):
        season = Trakt['shows'].season('not-found-4040', 1)

    assert season is None


def test_episode_basic():
    with HTTMock(mock.fixtures, mock.unknown):
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

    assert episode.runtime == 61


def test_episode_not_found():
    with HTTMock(mock.fixtures, mock.unknown):
        episode = Trakt['shows'].episode('not-found-4040', 1, 1)

    assert episode is None


def test_episode_proxy():
    with HTTMock(mock.fixtures, mock.unknown):
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
