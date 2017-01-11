from tests.core.helpers import read

from six.moves.urllib_parse import urlparse, parse_qsl
from trakt import Trakt
import responses


def lookup_callback(request):
    url = urlparse(request.url)

    try:
        return 200, {}, read('fixtures%s.json' % url.path)
    except:
        return 200, {}, '[]'


def query_callback(request):
    url = urlparse(request.url)
    query = dict(parse_qsl(url.query))

    if not query.get('query'):
        return 400, {}, '[]'

    # Build path
    if query.get('year'):
        path = 'fixtures%s/%s/%s.json' % (
            url.path,
            query['year'],
            query['query']
        )
    else:
        path = 'fixtures%s/%s.json' % (
            url.path,
            query['query']
        )

    # Return response
    try:
        return 200, {}, read(path)
    except:
        return 200, {}, '[]'


@responses.activate
def test_lookup_movie():
    responses.add_callback(
        responses.GET, 'http://mock/search/imdb/tt0848228',
        callback=lookup_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    movie = Trakt['search'].lookup('tt0848228', 'imdb')
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


@responses.activate
def test_lookup_show():
    responses.add_callback(
        responses.GET, 'http://mock/search/imdb/tt0903747',
        callback=lookup_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    show = Trakt['search'].lookup('tt0903747', 'imdb')
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


@responses.activate
def test_lookup_episode():
    responses.add_callback(
        responses.GET, 'http://mock/search/imdb/tt0959621',
        callback=lookup_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    episode = Trakt['search'].lookup('tt0959621', 'imdb')
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


@responses.activate
def test_query_movie():
    responses.add_callback(
        responses.GET, 'http://mock/search/movie',
        callback=query_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    movies = Trakt['search'].query('The Avengers', 'movie')

    assert [(m.score, (m.title, m.year)) for m in movies] == [
        (3419.5627,     ('The Avengers', 2012)),
        (58.450645,     ('Avengers: Age of Ultron', 2015)),
        (54.93378,      ('The Avengers', 1998)),
        (37.166332,     ('Captain America: The First Avenger', 2011)),
        (5.0396857,     ('Captain America: The Winter Soldier', 2014)),
        (1.4125466,     ('Captain America: Civil War', 2016)),
        (1.0787,        ('Ultimate Avengers', 2006)),
        (0.9917594,     ('X-Men Origins: Wolverine', 2009)),
        (0.84162766,    ('The Punisher', 2004)),
        (0.72275203,    ('Avengers Confidential: Black Widow & Punisher', 2014))
    ]


@responses.activate
def test_query_show():
    responses.add_callback(
        responses.GET, 'http://mock/search/show',
        callback=query_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    shows = Trakt['search'].query('Breaking Bad', 'show')

    assert [(s.score, (s.title, s.year)) for s in shows] == [
        (6795.639,      ('Breaking Bad', 2008)),
        (1.4921961,     ('Breaking In', 2011)),
        (0.15205674,    ('Talking Bad', 2013)),
        (0.023019673,   ('Good Times, Bad Times', 1990)),
        (0.00541616,    ('Mystery Science Theater 3000', 1988)),
        (0.0043216385,  ('What About Brian', 2006)),
        (0.0027682593,  ('Pinocchio', 2014)),
        (0.0014085078,  ('Benidorm', 2007)),
        (0.000756543,   ('Giant Killing', 2010)),
        (0.0006980828,  ('The Birthday Boys', 2013))
    ]


@responses.activate
def test_query_episode():
    responses.add_callback(
        responses.GET, 'http://mock/search/episode',
        callback=query_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    episodes = Trakt['search'].query('Breaking Bad', 'episode')

    assert [(e.score, (e.pk, e.title), (e.show.title, e.show.year)) for e in episodes] == [
        (120.28289, ((   5,  4),     'Pope Breaks Bad'),            ('Falling Skies', 2011)),
        (23.962301, ((2013, 10),    'Breaking Bad Special'),        ('MythBusters', 2003)),
        (21.605352, ((   2,  4),     "Charlie's Dad Breaks Bad"),   ('Anger Management', 2012)),
        (3.5197084, ((   1,  1),     'Breaking Bad'),               ("The Writers' Room", 2013)),
        (1.7284282, ((  12,  1),     'Breaking Bad Girls'),         ('Bad Girls Club', 2006)),
        (1.4575909, ((   8, 16),    'Bad Crazy'),                   ('How I Met Your Mother', 2005)),
        (1.2199193, ((   5, 16),    'Felina'),                      ('Breaking Bad', 2008)),
        (1.0844237, ((   5, 14),    'Ozymandias'),                  ('Breaking Bad', 2008)),
        (1.0452855, ((   1,  1),     'Pilot'),                      ('Breaking Bad', 2008)),
        (0.97547776, ((  5, 13),    "To'hajiilee"),                 ('Breaking Bad', 2008))
    ]
