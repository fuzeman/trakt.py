# flake8: noqa: E201

from tests.core import mock
from trakt import Trakt

from httmock import HTTMock


def test_lookup_movie():
    with HTTMock(mock.fixtures, mock.unknown):
        movies = Trakt['search'].lookup('tt0848228', 'imdb', extended='full')

    assert isinstance(movies, list)

    movie = movies[0]

    assert movie is not None

    assert movie.keys == [
        ('imdb', 'tt0848228'),
        ('tmdb', '24428'),
        ('slug', 'the-avengers-2012'),
        ('trakt', '14701')
    ]

    assert movie.title == "The Avengers"
    assert movie.year == 2012

    assert movie.overview is not None
    assert movie.score is None

    assert movie.rating is not None
    assert movie.rating.value == 8.30135
    assert movie.rating.votes == 27148


def test_lookup_show():
    with HTTMock(mock.fixtures, mock.unknown):
        shows = Trakt['search'].lookup('tt0903747', 'imdb', extended='full')

    assert isinstance(shows, list)

    show = shows[0]

    assert show is not None

    assert show.keys == [
        ('tvdb', '81189'),
        ('tmdb', '1396'),
        ('imdb', 'tt0903747'),
        ('tvrage', '18164'),
        ('slug', 'breaking-bad'),
        ('trakt', '1388')
    ]

    assert show.title == "Breaking Bad"
    assert show.year == 2008

    assert show.overview is not None
    assert show.score is None

    assert show.rating is not None
    assert show.rating.value == 9.42404
    assert show.rating.votes == 44177


def test_lookup_episode():
    with HTTMock(mock.fixtures, mock.unknown):
        episodes = Trakt['search'].lookup('tt0959621', 'imdb', extended='full')

    assert isinstance(episodes, list)

    episode = episodes[0]

    assert episode is not None

    assert episode.keys == [
        (1, 1),
        ('tvdb', '349232'),
        ('tmdb', '62085'),
        ('imdb', 'tt0959621'),
        ('tvrage', '637041'),
        ('trakt', '73482')
    ]

    assert episode.title == "Pilot"

    assert episode.overview is not None
    assert episode.score is None

    assert episode.rating is not None
    assert episode.rating.value == 8.44087
    assert episode.rating.votes == 4854

    assert episode.show.keys == [
        ('tvdb', '81189'),
        ('tmdb', '1396'),
        ('imdb', 'tt0903747'),
        ('tvrage', '18164'),
        ('slug', 'breaking-bad'),
        ('trakt', '1388')
    ]

    assert episode.show.title == "Breaking Bad"
    assert episode.show.year == 2008

    assert episode.show.rating is not None
    assert episode.show.rating.value == 9.42404
    assert episode.show.rating.votes == 44177


def test_query_movie():
    with HTTMock(mock.fixtures, mock.unknown):
        movies = Trakt['search'].query('The Avengers', 'movie')

    assert [(m.score, (m.title, m.year)) for m in movies] == [
        (3553.1072,     ('The Avengers', 2012)),
        (61.41709,      ('Avengers: Age of Ultron', 2015)),
        (58.241222,     ('The Avengers', 1998)),
        (38.641922,     ('Captain America: The First Avenger', 2011)),
        (5.2409315,     ('Captain America: The Winter Soldier', 2014)),
        (1.5118352,     ('Captain America: Civil War', 2016)),
        (1.1865233,     ('Ultimate Avengers', 2006)),
        (1.0413905,     ('X-Men Origins: Wolverine', 2009)),
        (0.88450277,    ('The Punisher', 2004)),
        (0.77113676,    ('Avengers Grimm', 2015))
    ]


def test_query_show():
    with HTTMock(mock.fixtures, mock.unknown):
        shows = Trakt['search'].query('Breaking Bad', 'show')

    assert [(s.score, (s.title, s.year)) for s in shows] == [
        (6935.3633,     ('Breaking Bad', 2008)),
        (1.4982065,     ('Breaking In', 2011)),
        (0.15576369,    ('Talking Bad', 2013)),
        (0.023026062,   ('Good Times, Bad Times', 1990)),
        (0.005517228,   ('Mystery Science Theater 3000', 1988)),
        (0.004323423,   ('What About Brian', 2006)),
        (0.0029597091,  ('Pinocchio', 2014)),
        (0.0014896033,  ('Benidorm', 2007)),
        (0.00077344314, ('Giant Killing', 2010)),
        (0.00069781754, ('The Birthday Boys', 2013))
    ]


def test_query_episode():
    with HTTMock(mock.fixtures, mock.unknown):
        episodes = Trakt['search'].query('Breaking Bad', 'episode')

    assert [(e.score, (e.pk, e.title), (e.show.title, e.show.year)) for e in episodes] == [
        (122.190025, ((   5,  4),   'Pope Breaks Bad'),             ('Falling Skies', 2011)),
        (24.123692,  ((2013, 10),   'Breaking Bad Special'),        ('MythBusters', 2003)),
        (22.002064,  ((   2,  4),   "Charlie's Dad Breaks Bad"),    ('Anger Management', 2012)),
        (3.5203302,  ((   1,  1),   'Breaking Bad'),                ("The Writers' Room", 2013)),
        (1.7287335,  ((  12,  1),   'Breaking Bad Girls'),          ('Bad Girls Club', 2006)),
        (1.5032781,  ((   8, 16),   'Bad Crazy'),                   ('How I Met Your Mother', 2005)),
        (1.2728773,  ((   5, 16),   'Felina'),                      ('Breaking Bad', 2008)),
        (1.1314209,  ((   5, 14),   'Ozymandias'),                  ('Breaking Bad', 2008)),
        (1.1256235,  ((   1,  1),   'Pilot'),                       ('Breaking Bad', 2008)),
        (1.0210383,  ((  5,  13),   "To'hajiilee"),                 ('Breaking Bad', 2008))
    ]
