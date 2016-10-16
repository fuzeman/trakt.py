from hamcrest import *
from trakt import Trakt
import responses


@responses.activate
def test_missing_media_parameter():
    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        assert_that(calling(Trakt['sync/history'].get).with_args(id='1'), raises(ValueError))
