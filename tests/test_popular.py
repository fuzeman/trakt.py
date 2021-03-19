# flake8: noqa: E241

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock


def test_movie():
    with HTTMock(mock.fixtures, mock.unknown):
        movies = Trakt['movies'].popular()

    assert [(m.title, m.year) for m in movies] == [
        ("Deadpool", 2016),
        ("The Dark Knight", 2008),
        ("Inception", 2010),
        ("Guardians of the Galaxy", 2014),
        ("The Avengers", 2012),
        ("The Matrix", 1999),
        ("Interstellar", 2014),
        ("Suicide Squad", 2016),
        ("Star Wars: The Force Awakens", 2015),
        ("Frozen", 2013)
    ]


def test_show():
    with HTTMock(mock.fixtures, mock.unknown):
        shows = Trakt['shows'].popular()

    assert [(m.title, m.year) for m in shows] == [
        ("Game of Thrones", 2011),
        ("Breaking Bad", 2008),
        ("The Walking Dead", 2010),
        ("The Big Bang Theory", 2007),
        ("Dexter", 2006),
        ("Sherlock", 2010),
        ("How I Met Your Mother", 2005),
        ("Arrow", 2012),
        ("Friends", 1994),
        ("Homeland", 2011)
    ]
