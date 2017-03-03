# flake8: noqa: E241

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock


def test_movie():
    with HTTMock(mock.fixtures, mock.unknown):
        movies = Trakt['movies'].trending()

    assert [(m.watchers, m.title, m.year) for m in movies] == [
        (78,    "Moana", 2016),
        (64,    "Passengers", 2016),
        (62,    "Fantastic Beasts and Where to Find Them", 2016),
        (55,    "Doctor Strange", 2016),
        (55,    "Moonlight", 2016),
        (47,    "Trolls", 2016),
        (47,    "Resident Evil: The Final Chapter", 2016),
        (44,    "Hacksaw Ridge", 2016),
        (44,    "Arrival", 2016),
        (37,    "Assassin's Creed", 2016)
    ]


def test_show():
    with HTTMock(mock.fixtures, mock.unknown):
        shows = Trakt['shows'].trending()

    assert [(m.watchers, m.title, m.year) for m in shows] == [
        (215,   "The Flash", 2014),
        (158,   "The Walking Dead", 2010),
        (111,   "The Big Bang Theory", 2007),
        (99,    "Homeland", 2011),
        (86,    "Shameless", 2011),
        (84,    "Taboo", 2017),
        (78,    "Supergirl", 2015),
        (74,    "Scorpion", 2014),
        (71,    "The 100", 2014),
        (69,    "Game of Thrones", 2011)
    ]
