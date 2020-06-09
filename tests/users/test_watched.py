# flake8: noqa: F403, F405
from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt
from trakt.objects import Movie, Show, Season, Episode

from datetime import datetime
from dateutil.tz import tzutc
from hamcrest import *
from httmock import HTTMock
import pytest


def test_shows():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['users/*/watched'].get('me', 'shows')

            assert items is not None

            items = list(items)

    assert_that(items, all_of(
        has_length(2),
        contains(
            all_of(
                instance_of(Show),
                has_properties({
                    'title': 'Breaking Bad',
                    'year': 2008,

                    'plays': 56,

                    # Timestamps
                    'last_watched_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc()),
                    'last_updated_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc()),
                    'reset_at': None,

                    # Keys
                    'keys': [
                        ('tvdb', '81189'),
                        ('tmdb', '1396'),
                        ('imdb', 'tt0903747'),
                        ('slug', 'breaking-bad'),
                        ('trakt', '1')
                    ],

                    # Seasons
                    'seasons': has_entries({
                        1: all_of(
                            instance_of(Season),
                            has_properties({
                                'pk': 1,

                                # Episodes
                                'episodes': has_entries({
                                    1: all_of(
                                        instance_of(Episode),
                                        has_properties({
                                            'pk': (1, 1),

                                            'plays': 1,

                                            # Timestamps
                                            'last_watched_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc())
                                        })
                                    ),
                                    2: all_of(
                                        instance_of(Episode),
                                        has_properties({
                                            'pk': (1, 2),

                                            'plays': 1,

                                            # Timestamps
                                            'last_watched_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc())
                                        })
                                    )
                                })
                            })
                        ),
                        2: all_of(
                            instance_of(Season),
                            has_properties({
                                'pk': 2,

                                # Episodes
                                'episodes': has_entries({
                                    1: all_of(
                                        instance_of(Episode),
                                        has_properties({
                                            'pk': (2, 1),

                                            'plays': 1,

                                            # Timestamps
                                            'last_watched_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc())
                                        })
                                    ),
                                    2: all_of(
                                        instance_of(Episode),
                                        has_properties({
                                            'pk': (2, 2),

                                            'plays': 1,

                                            # Timestamps
                                            'last_watched_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc())
                                        })
                                    )
                                })
                            })
                        )
                    })
                })
            ),
            all_of(
                instance_of(Show),
                has_properties({
                    'title': 'Parks and Recreation',
                    'year': 2009,

                    'plays': 23,

                    # Timestamps
                    'last_watched_at': datetime(2014, 10, 12, 17, 0, 54, tzinfo=tzutc()),
                    'last_updated_at': datetime(2014, 10, 12, 17, 0, 54, tzinfo=tzutc()),
                    'reset_at': None,

                    # Keys
                    'keys': [
                        ('tvdb', '84912'),
                        ('tmdb', '8592'),
                        ('imdb', 'tt1266020'),
                        ('slug', 'parks-and-recreation'),
                        ('trakt', '4')
                    ],

                    # Seasons
                    'seasons': has_entries({
                        1: all_of(
                            instance_of(Season),
                            has_properties({
                                'pk': 1,

                                # Episodes
                                'episodes': has_entries({
                                    1: all_of(
                                        instance_of(Episode),
                                        has_properties({
                                            'pk': (1, 1),

                                            'plays': 1,

                                            # Timestamps
                                            'last_watched_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc())
                                        })
                                    ),
                                    2: all_of(
                                        instance_of(Episode),
                                        has_properties({
                                            'pk': (1, 2),

                                            'plays': 1,

                                            # Timestamps
                                            'last_watched_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc())
                                        })
                                    )
                                })
                            })
                        ),
                        2: all_of(
                            instance_of(Season),
                            has_properties({
                                'pk': 2,

                                # Episodes
                                'episodes': has_entries({
                                    1: all_of(
                                        instance_of(Episode),
                                        has_properties({
                                            'pk': (2, 1),

                                            'plays': 1,

                                            # Timestamps
                                            'last_watched_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc())
                                        })
                                    ),
                                    2: all_of(
                                        instance_of(Episode),
                                        has_properties({
                                            'pk': (2, 2),

                                            'plays': 1,

                                            # Timestamps
                                            'last_watched_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc())
                                        })
                                    )
                                })
                            })
                        )
                    })
                })
            )
        )
    ))


def test_movies():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['users/*/watched'].get('me', 'movies')

            assert items is not None

            items = list(items)

    assert_that(items, all_of(
        has_length(2),
        contains(
            all_of(
                instance_of(Movie),
                has_properties({
                    'pk': ('imdb', 'tt0372784'),
                    'title': 'Batman Begins',
                    'year': 2005,

                    'plays': 4,

                    # Timestamps
                    'last_watched_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc()),
                    'last_updated_at': datetime(2014, 10, 11, 17, 0, 54, tzinfo=tzutc()),

                    # Keys
                    'keys': [
                        ('imdb', 'tt0372784'),
                        ('tmdb', '272'),
                        ('slug', 'batman-begins-2005'),
                        ('trakt', '6')
                    ]
                })
            ),
            all_of(
                instance_of(Movie),
                has_properties({
                    'pk': ('imdb', 'tt0468569'),
                    'title': 'The Dark Knight',
                    'year': 2008,

                    'plays': 2,

                    # Timestamps
                    'last_watched_at': datetime(2014, 10, 12, 17, 0, 54, tzinfo=tzutc()),
                    'last_updated_at': datetime(2014, 10, 12, 17, 0, 54, tzinfo=tzutc()),

                    # Keys
                    'keys': [
                        ('imdb', 'tt0468569'),
                        ('tmdb', '155'),
                        ('slug', 'the-dark-knight-2008'),
                        ('trakt', '4')
                    ]
                })
            )
        )
    ))


def test_invalid_media():
    with pytest.raises(ValueError):
        items = Trakt['users/*/watched'].get('me')

    with pytest.raises(ValueError):
        items = Trakt['users/*/watched'].get('me', 'episodes')
