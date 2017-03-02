# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt
from trakt.objects import Show, Season, Episode

from hamcrest import *
from httmock import HTTMock


def test_watched():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['users/me/lists/shows'].items()

    # Ensure collection is valid
    assert_that(items, not_none())
    assert_that(items, has_length(3))

    # Validate items
    assert_that(items, contains(
        # Game of Thrones (2011)
        all_of(
            instance_of(Show),
            has_properties({
                'pk': ('tvdb', '121361'),
                'title': 'Game of Thrones',
                'year': 2011,

                # Keys
                'keys': [
                    ('tvdb', '121361'),
                    ('tmdb', '1399'),
                    ('imdb', 'tt0944947'),
                    ('tvrage', '24493'),
                    ('slug', 'game-of-thrones'),
                    ('trakt', '1390')
                ]
            })
        ),

        # Game of Thrones (2011) - S05
        all_of(
            instance_of(Season),
            has_properties({
                'pk': 5,

                # Keys
                'keys': [
                    5,
                    ('tmdb', '62090'),
                    ('trakt', '3967')
                ]
            })
        ),

        # Game of Thrones (2011) - S05E04
        all_of(
            instance_of(Episode),
            has_properties({
                'pk': (5, 4),

                # Keys
                'keys': [
                    (5, 4),
                    ('tvdb', '5150183'),
                    ('tmdb', '1045553'),
                    ('imdb', 'tt3866838'),
                    ('tvrage', '1065765456'),
                    ('trakt', '1782362')
                ]
            })
        )
    ))
