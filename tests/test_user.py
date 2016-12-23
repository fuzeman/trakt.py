from tests.core.helpers import read

from trakt import Trakt
import pytest
import responses


@responses.activate
def test_likes():
    responses.add(
        responses.GET, 'http://mock/users/likes',
        body=read('fixtures/users/likes.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        likes = Trakt['users'].likes()
        assert likes is not None

        likes = list(likes)
        assert len(likes) is 3

    assert likes[0].keys == [
        ('trakt', 1519)
    ]

    assert likes[1].keys == [
        ('trakt', '1238362'),
        ('slug', 'star-wars-machete')
    ]

    assert likes[2].keys == [
        ('trakt', '840781'),
        ('slug', 'star-wars-timeline')
    ]


@responses.activate
def test_likes_invalid_response():
    responses.add(
        responses.GET, 'http://mock/users/likes',
        body='Not Found', status=404,
        content_type='text/html'
    )

    Trakt.base_url = 'http://mock'

    likes = Trakt['users'].likes()
    assert likes is not None

    likes = list(likes)
    assert len(likes) is 0


def test_likes_invalid_type():
    Trakt.base_url = 'http://mock'

    with pytest.raises(ValueError):
        likes = Trakt['users'].likes('invalid')
        assert likes is not None

        likes = list(likes)
