from tests.core.helpers import read

from trakt import Trakt
import responses


@responses.activate
def test_movie():
    responses.add(
        responses.GET, 'http://mock/movies/trending',
        body=read('fixtures/movies/trending.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    movies = Trakt['movies'].trending()

    assert len(movies) == 10

    assert [(m.watchers, m.title, m.year) for m in movies] == [
        (24, "Cinderella", 2015),
        (15, "Pleasure or Pain", 2013),
        (14, "Get Hard", 2015),
        (12, "Mad Max: Fury Road", 2015),
        (11, "Maggie", 2015),
        (10, "The Gunman", 2015),
        (9, "Ex Machina", 2015),
        (8, "The SpongeBob Movie: Sponge Out of Water", 2015),
        (7, "Chappie", 2015),
        (6, "While We're Young", 2015)
    ]


@responses.activate
def test_show():
    responses.add(
        responses.GET, 'http://mock/shows/trending',
        body=read('fixtures/shows/trending.json'), status=200,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    shows = Trakt['shows'].trending()

    assert len(shows) == 10

    assert [(m.watchers, m.title, m.year) for m in shows] == [
        (45, "Orange Is the New Black", 2013),
        (42, "Game of Thrones", 2011),
        (35, "True Detective", 2014),
        (21, "Pretty Little Liars", 2010),
        (21, "Sense8", 2015),
        (21, "The Last Ship", 2014),
        (17, "Arrow", 2012),
        (14, "The Big Bang Theory", 2007),
        (13, "Tyrant", 2014),
        (12, "Grey's Anatomy", 2005)
    ]
