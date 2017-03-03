from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock


def test_start():
    with HTTMock(mock.scrobble_start, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['scrobble'].start(
                movie={'ids': {'tmdb': 76341}},
                progress=0.35
            )

    assert result is not None

    assert result.get('action') == 'start'

    assert result.get('id') == 9832
    assert result.get('progress') == 0.35


def test_pause():
    with HTTMock(mock.scrobble_pause, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['scrobble'].pause(
                movie={'ids': {'tmdb': 76341}},
                progress=35.86
            )

    assert result is not None

    assert result.get('action') == 'pause'

    assert result.get('id') == 9832
    assert result.get('progress') == 35.86


def test_stop():
    with HTTMock(mock.scrobble_stop, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['scrobble'].stop(
                movie={'ids': {'tmdb': 76341}},
                progress=97.45
            )

    assert result is not None

    assert result.get('action') == 'stop'

    assert result.get('id') == 9832
    assert result.get('progress') == 97.45
