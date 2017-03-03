# flake8: noqa: E221

from tests.core import mock
from trakt import Trakt

from hamcrest import *
from httmock import HTTMock


def test_basic():
    with HTTMock(mock.sync_get, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            collection = Trakt['sync/playback'].get()

    # Ensure collection is valid
    assert_that(collection, not_none())
    
    # Batman Begins (2005)
    assert_that(collection[('imdb', 'tt0372784')], has_properties({
        'id': 13
    }))
    
    # Breaking Bad (2008)
    assert_that(collection[('tvdb', '81189')], has_properties({
        # Seasons
        'seasons': all_of(
            has_length(1),

            # Seasons
            has_entry(0, has_properties({
                'episodes': all_of(
                    has_length(1),

                    # Episodes
                    has_entry(1, has_properties({
                        'id': 37
                    }))
                )
            }))
        ),
    }))

    # Delete progress items
    with HTTMock(mock.sync_playback_delete, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            success_movie   = Trakt['sync/playback'].delete(13)
            success_episode = Trakt['sync/playback'].delete(37)

    assert success_movie is True
    assert success_episode is True
