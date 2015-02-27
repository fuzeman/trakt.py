from trakt.interfaces.base import Interface

import responses
import requests


@responses.activate
def test_content_type():
    responses.add(
        responses.GET, 'http://mock/test',
        body='{"test": True}', status=502,
        content_type=None
    )

    r = requests.get('http://mock/test')

    data = Interface.get_data(r)
    assert data is None
