
from tests.core import mock
from trakt import Trakt

from hamcrest import *
from httmock import HTTMock


def assert_valid_result(result):
    assert_that(result, has_entries({
        "added": {
            "movies": 1,
            "shows": 2,
            "seasons": 2,
            "users": 0
            },
        "not_found": {
            "movies": [
                {
                "ids": {
                    "imdb": "tt0000111"
                }
                }
            ],
            "shows": [],
            "seasons": [],
            "users": []
        }
    }))

def test_add_hidden_in_calendar():
    with HTTMock(mock.hidden_add, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['users/hidden/calendar'].add(items={'shows': [{'ids': {'trakt': 48 }}]})
    assert_valid_result(result)

def test_add_hidden_in_progress_watched():
    with HTTMock(mock.hidden_add, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['users/hidden/progress_watched'].add(items={'shows': [{'ids': {'trakt': 48 }}]})
    assert_valid_result(result)


def test_add_hidden_in_progress_collected():
    with HTTMock(mock.hidden_add, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['users/hidden/progress_collected'].add(items={'shows': [{'ids': {'trakt': 48 }}]})
    assert_valid_result(result)


def test_add_hidden_in_recommendations():
    with HTTMock(mock.hidden_add, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['users/hidden/recommendations'].add(items={'shows': [{'ids': {'trakt': 48 }}]})
    assert_valid_result(result)


def test_add_hidden_in_comments():
    with HTTMock(mock.hidden_add, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            result = Trakt['users/hidden/comments'].add(items={'users': [{'ids': {'slug': 'sean' }}]})
    assert_valid_result(result)