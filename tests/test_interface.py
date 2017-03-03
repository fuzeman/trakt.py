from __future__ import absolute_import, division, print_function

from trakt.core import exceptions
from trakt.interfaces.base import Interface

from httmock import HTTMock
import httmock
import pytest
import requests


@httmock.urlmatch(netloc='mock', path='/test')
def client_error(url, request):
    return httmock.response(404, '{"test": True}')


@httmock.urlmatch(netloc='mock', path='/test')
def server_error(url, request):
    return httmock.response(502, '{"test": True}')


def test_missing_content_type():
    with HTTMock(server_error):
        response = requests.get('http://mock/test')

    data = Interface(None).get_data(response)
    assert data is None


def test_server_error():
    with HTTMock(server_error):
        response = requests.get('http://mock/test')

    with pytest.raises(exceptions.ServerError):
        Interface(None).get_data(response, exceptions=True)


def test_client_error():
    with HTTMock(client_error):
        response = requests.get('http://mock/test')

    with pytest.raises(exceptions.ClientError):
        Interface(None).get_data(response, exceptions=True)
