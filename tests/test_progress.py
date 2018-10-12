from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from hamcrest import assert_that, has_entries
from httmock import HTTMock


def test_progress_watched():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            progress = Trakt['shows'].progress_watched(1390)

    assert progress is not None
    assert progress.reset_at is not None
    assert progress.last_progress_change is not None
    assert progress.aired == 10
    assert progress.completed == 6

    assert len(progress.seasons) == 1
    assert progress.seasons[1].aired == 8
    assert progress.seasons[1].completed == 6

    assert len(progress.seasons[1].episodes) == 10
    assert progress.seasons[1].episodes[1].progress_timestamp is not None

    assert len(progress.hidden_seasons) == 0

    # Next Episode
    assert progress.next_episode is not None
    assert progress.next_episode.pk == (1, 7)

    assert progress.next_episode.keys == [
        (1, 7),

        ('tvdb', '3436461'),
        ('tmdb', '63062'),
        ('imdb', 'tt1837863'),
        ('tvrage', '1065036404'),
        ('trakt', '73646')
    ]

    assert_that(progress.next_episode.to_dict(), has_entries({
        'number': 7,
        'title': 'You Win or You Die',
        'ids': {
            'trakt': '73646',
            'tvrage': '1065036404',
            'tvdb': '3436461',
            'tmdb': '63062',
            'imdb': 'tt1837863'
        }
    }))

# Last Episode
    assert progress.last_episode is not None
    assert progress.last_episode.pk == (1, 5)

    assert progress.last_episode.keys == [
        (1, 5),

        ('tvdb', '3436461'),
        ('tmdb', '63062'),
        ('imdb', 'tt1837863'),
        ('tvrage', '1065036404'),
        ('trakt', '73646')
    ]

    assert_that(progress.last_episode.to_dict(), has_entries({
        'number': 5,
        'title': 'You Die and You Win',
        'ids': {
            'trakt': '73646',
            'tvrage': '1065036404',
            'tvdb': '3436461',
            'tmdb': '63062',
            'imdb': 'tt1837863'
        }
    }))


def test_progress_watched_plus_hidden():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            progress = Trakt['shows'].progress_watched('game-of-thrones', hidden=True)

    assert progress is not None
    assert progress.reset_at is None

    assert len(progress.hidden_seasons) == 1

    assert_that(progress.to_dict(), has_entries({
        'aired': 10,
        'completed': 6,
        'last_watched_at': '2015-03-21T19:03:58.000-00:00',
        'reset_at': None,
        'seasons': [
            {
                'number': 1,
                'aired': 8,
                'completed': 6,
                'episodes': [
                    {
                        'number': 1,
                        'completed': True,
                        'last_watched_at': '2015-03-21T19:03:58.000-00:00'
                    },
                    {
                        'number': 2,
                        'completed': True,
                        'last_watched_at': '2015-03-21T19:03:58.000-00:00'
                    },
                    {
                        'number': 3,
                        'completed': True,
                        'last_watched_at': '2015-03-21T19:03:58.000-00:00'
                    },
                    {
                        'number': 4,
                        'completed': True,
                        'last_watched_at': '2015-03-21T19:03:58.000-00:00'
                    },
                    {
                        'number': 5,
                        'completed': True,
                        'last_watched_at': '2015-03-21T19:03:58.000-00:00'
                    },
                    {
                        'number': 6,
                        'completed': True,
                        'last_watched_at': '2015-03-21T19:03:58.000-00:00'
                    },
                    {
                        'number': 7,
                        'completed': False,
                        'last_watched_at': None
                    },
                    {
                        'number': 8,
                        'completed': False,
                        'last_watched_at': None
                    },
                    {
                        'number': 9,
                        'completed': False,
                        'last_watched_at': None
                    },
                    {
                        'number': 10,
                        'completed': False,
                        'last_watched_at': None
                    }
                ]
            }
        ],
        'hidden_seasons': [
            {
                'number': 2,
                'ids': {
                    'trakt': '3051',
                    'tvdb': '498968',
                    'tmdb': '53334'
                }
            }
        ],
        'next_episode': {
            'season': 1,
            'number': 7,
            'title': 'You Win or You Die',
            'ids': {
                'trakt': '73646',
                'tvdb': '3436461',
                'imdb': 'tt1837863',
                'tmdb': '63062',
                'tvrage': '1065036404'
            }
        }
    }))


def test_progress_collection():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            progress = Trakt['shows'].progress_collection(1390)

    assert progress is not None
    assert progress.reset_at is None
    assert progress.last_progress_change is not None

    assert progress.seasons[1].episodes[1].progress_timestamp is not None

    # Next Episode
    assert progress.next_episode is not None
    assert progress.next_episode.pk == (1, 7)

    assert progress.next_episode.keys == [
        (1, 7),

        ('tvdb', '3436461'),
        ('tmdb', '63062'),
        ('imdb', 'tt1837863'),
        ('tvrage', '1065036404'),
        ('trakt', '73646')
    ]

    assert_that(progress.next_episode.to_dict(), has_entries({
        'number': 7,
        'title': 'You Win or You Die',
        'ids': {
            'trakt': '73646',
            'tvrage': '1065036404',
            'tvdb': '3436461',
            'tmdb': '63062',
            'imdb': 'tt1837863'
        }
    }))
