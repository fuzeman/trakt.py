# flake8: noqa: F403, F405

from trakt import Trakt

from hamcrest import *
import responses


@responses.activate
def test_missing_media_parameter():
    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        assert_that(calling(Trakt['sync/watched'].get), raises(ValueError))
