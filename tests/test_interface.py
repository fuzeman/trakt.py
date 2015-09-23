from trakt.core import exceptions
from trakt.interfaces.base import Interface

import pytest
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


@responses.activate
def test_server_error():
    responses.add(
        responses.GET, 'http://mock/test',
        body='{"test": True}', status=502,
        content_type=None
    )

    r = requests.get('http://mock/test')

    with pytest.raises(exceptions.ServerError):
        Interface.get_data(r, exceptions=True)


@responses.activate
def test_client_error():
    responses.add(
        responses.GET, 'http://mock/test',
        body='{"test": True}', status=404,
        content_type=None
    )

    r = requests.get('http://mock/test')

    with pytest.raises(exceptions.ClientError):
        Interface.get_data(r, exceptions=True)
