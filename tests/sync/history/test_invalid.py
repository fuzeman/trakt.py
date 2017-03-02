# flake8: noqa: F403, F405

from tests.core import mock
from trakt import Trakt

from hamcrest import *
from httmock import HTTMock


def test_missing_media_parameter():
    with HTTMock(mock.fixtures, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            assert_that(calling(Trakt['sync/history'].get).with_args(id='1'), raises(ValueError))
