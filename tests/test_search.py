from tests.core.helpers import read

from six.moves.urllib_parse import urlparse, parse_qsl
from trakt import Trakt
import responses


def search_callback(request):
    url = urlparse(request.url)
    query = dict(parse_qsl(url.query))

    if 'id' in query and 'id_type' in query:
        path = 'fixtures/search/lookup/%s/%s.json' % (
            query.get('id_type'),
            query.get('id')
        )
    else:
        path = 'fixtures/search/query/%s/%s/%s.json' % (
            query.get('type', 'all'),
            query.get('year', 'all'),
            query.get('query')
        )

    try:
        content = read(path)
        return 200, {}, content
    except:
        return 200, {}, '[]'


@responses.activate
def test_lookup_movie():
    responses.add_callback(
        responses.GET, 'http://mock/search',
        callback=search_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    movie = Trakt['search'].lookup('tt0848228', 'imdb')

    assert movie.keys == [
        ('imdb', 'tt0848228'),
        ('tmdb', '24428'),
        ('slug', 'the-avengers-2012'),
        ('trakt', '14701')
    ]

    assert movie.title == "The Avengers"
    assert movie.year == 2012

    assert sorted(movie.images.keys()) == ['fanart', 'poster']
    assert movie.overview is not None
    assert movie.score is None


@responses.activate
def test_lookup_show():
    responses.add_callback(
        responses.GET, 'http://mock/search',
        callback=search_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    show = Trakt['search'].lookup('tt0903747', 'imdb')

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

    assert sorted(show.images.keys()) == ['fanart', 'poster']
    assert show.overview is not None
    assert show.score is None


@responses.activate
def test_lookup_episode():
    responses.add_callback(
        responses.GET, 'http://mock/search',
        callback=search_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    episode = Trakt['search'].lookup('tt0959621', 'imdb')

    assert episode.keys == [
        (1, 1),
        ('tvdb', '349232'),
        ('tmdb', '62085'),
        ('imdb', 'tt0959621'),
        ('tvrage', '637041'),
        ('trakt', '73482')
    ]

    assert episode.title == "Pilot"

    assert sorted(episode.images.keys()) == ['screenshot']
    assert episode.overview is not None
    assert episode.score is None

    assert episode.show.keys == [
        ('slug', 'breaking-bad'),
        ('trakt', '1388')
    ]

    assert episode.show.title == "Breaking Bad"
    assert episode.show.year == 2008

    assert sorted(episode.show.images.keys()) == ['fanart', 'poster']


@responses.activate
def test_query_movie():
    responses.add_callback(
        responses.GET, 'http://mock/search',
        callback=search_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    movies = Trakt['search'].query('The Avengers', 'movie')

    assert [(m.score, (m.title, m.year)) for m in movies] == [
        (77.052734, ('Avenged', None)),
        (77.0176,   ('Avenger', 2006)),
        (60.26589,  ('The Avengers', 2012)),
        (60.26589,  ('The Avengers', 1998)),
        (60.26589,  ('The Avenger', 1960)),
        (60.26589,  ('The Avenger', 1931)),
        (60.26589,  ('The Avenging', 1982)),
        (60.26589,  ('The Avenger', 1947)),
        (55.793285, ('Invisible Avenger', 1954)),
        (55.652233, ('Crippled Avengers', 1978))
    ]


@responses.activate
def test_query_show():
    responses.add_callback(
        responses.GET, 'http://mock/search',
        callback=search_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    shows = Trakt['search'].query('Breaking Bad', 'show')

    assert [(s.score, (s.title, s.year)) for s in shows] == [
        (54.809517,     ('Breaking Bad', 2008)),
        (28.975079,     ('Breaking Boston', 2014)),
        (28.89469,      ('Breaking In', 2011)),
        (26.28082,      ('Talking Bad', 2013)),
        (20.346865,     ('Donal MacIntyre: Breaking Crime', 2015)),
        (18.345793,     ('Good Times, Bad Times', 1990)),
        (1.1290063,     ('What About Brian', 2006)),
        (0.39297247,    ('It Could Be Worse', 2013)),
        (0.39297247,    ('Murder Police', None)),
        (0.3438509,     ('Pinocchio', 2014))
    ]


@responses.activate
def test_query_episode():
    responses.add_callback(
        responses.GET, 'http://mock/search',
        callback=search_callback,
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    episodes = Trakt['search'].query('Breaking Bad', 'episode')

    assert [(e.score, (e.pk, e.title), (e.show.title, e.show.year)) for e in episodes] == [
        (77.16374, ((2, 13),    'Bad Breaks'),     ('Burn Notice', 2007)),
        (77.16374, ((1, 1),     'Breaking Bad'),   ("The Writers' Room", 2013)),
        (77.16374, ((2, 18),    'Breaking Bad'),   ('Honest Trailers', 2012)),
        (77.16374, ((4, 7),     'Bad Break'),      ('Bad Girls Club', 2006)),
        (77.16374, ((1, 8),     'Bad Break'),      ('Miami Ink', 2005)),
        (77.16374, ((2, 6),     'Breaking Bad'),   ('Pawn Stars UK', 2013)),
        (77.16374, ((6, 16),    'Bad Breaks'),     ('Trapper John, M.D.', 1979)),
        (77.16374, ((3, 8),     'Breaking Bad'),   ('Bad Days', 1969)),
        (77.16374, ((1, 261),   'Breaking Bad'),   ('The Totally Rad Show', 2007)),
        (77.16374, ((1, 2),     ' Breaking Bad'),  ('Fight Factory', 2012))
    ]
