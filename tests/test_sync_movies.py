from tests.core.helpers import authenticated_response

from datetime import datetime
from dateutil.tz import tzutc
from trakt import Trakt
import responses


@responses.activate
def test_playback():
    responses.add_callback(
        responses.GET, 'http://mock/sync/playback/movies',
        callback=authenticated_response('fixtures/sync/playback/movies.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        playback = Trakt['sync/playback'].movies()

    assert playback is not None

    # TRON: Legacy (2010)
    assert playback[('imdb', 'tt1104001')].title == 'TRON: Legacy'
    assert playback[('imdb', 'tt1104001')].year == 2010

    assert playback[('imdb', 'tt1104001')].pk == ('imdb', 'tt1104001')
    assert playback[('imdb', 'tt1104001')].keys == [
        ('imdb', 'tt1104001'),
        ('tmdb', '20526'),
        ('slug', 'tron-legacy-2010'),
        ('trakt', '12601')
    ]

    assert playback[('imdb', 'tt1104001')].progress == 64.0
    assert playback[('imdb', 'tt1104001')].paused_at == datetime(2015, 2, 9, 5, 56, 58, tzinfo=tzutc())

    # 100 Bloody Acres (2012)
    assert playback[('imdb', 'tt2290065')].title == '100 Bloody Acres'
    assert playback[('imdb', 'tt2290065')].year == 2012

    assert playback[('imdb', 'tt2290065')].pk == ('imdb', 'tt2290065')
    assert playback[('imdb', 'tt2290065')].keys == [
        ('imdb', 'tt2290065'),
        ('tmdb', '126757'),
        ('slug', '100-bloody-acres-2012'),
        ('trakt', '86920')
    ]

    assert playback[('imdb', 'tt2290065')].progress == 0.0
    assert playback[('imdb', 'tt2290065')].paused_at == datetime(2015, 1, 10, 6, 44, 9, tzinfo=tzutc())


@responses.activate
def test_collection():
    responses.add_callback(
        responses.GET, 'http://mock/sync/collection/movies',
        callback=authenticated_response('fixtures/sync/collection/movies.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        collection = Trakt['sync/collection'].movies()

    assert collection is not None

    # TRON: Legacy (2010)
    assert collection[('imdb', 'tt1104001')].title == 'TRON: Legacy'
    assert collection[('imdb', 'tt1104001')].year == 2010

    assert collection[('imdb', 'tt1104001')].pk == ('imdb', 'tt1104001')
    assert collection[('imdb', 'tt1104001')].keys == [
        ('imdb', 'tt1104001'),
        ('tmdb', '20526'),
        ('slug', 'tron-legacy-2010'),
        ('trakt', '12601')
    ]

    assert collection[('imdb', 'tt1104001')].is_collected
    assert collection[('imdb', 'tt1104001')].collected_at == datetime(2014, 9, 28, 22, 45, 23, tzinfo=tzutc())

    # 100 Bloody Acres (2012)
    assert collection[('imdb', 'tt2290065')].title == '100 Bloody Acres'
    assert collection[('imdb', 'tt2290065')].year == 2012

    assert collection[('imdb', 'tt2290065')].pk == ('imdb', 'tt2290065')
    assert collection[('imdb', 'tt2290065')].keys == [
        ('imdb', 'tt2290065'),
        ('tmdb', '126757'),
        ('slug', '100-bloody-acres-2012'),
        ('trakt', '86920')
    ]

    assert collection[('imdb', 'tt2290065')].is_collected
    assert collection[('imdb', 'tt2290065')].collected_at == datetime(2014, 1, 20, 7, 4, 4, tzinfo=tzutc())


@responses.activate
def test_ratings():
    responses.add_callback(
        responses.GET, 'http://mock/sync/ratings/movies',
        callback=authenticated_response('fixtures/sync/ratings/movies.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        ratings = Trakt['sync/ratings'].movies()

    assert ratings is not None

    # 100 Bloody Acres (2012)
    assert ratings[('imdb', 'tt2290065')].title == '100 Bloody Acres'
    assert ratings[('imdb', 'tt2290065')].year == 2012

    assert ratings[('imdb', 'tt2290065')].pk == ('imdb', 'tt2290065')
    assert ratings[('imdb', 'tt2290065')].keys == [
        ('imdb', 'tt2290065'),
        ('tmdb', '126757'),
        ('slug', '100-bloody-acres-2012'),
        ('trakt', '86920')
    ]

    assert ratings[('imdb', 'tt2290065')].rating.value == 8
    assert ratings[('imdb', 'tt2290065')].rating.timestamp == datetime(2015, 1, 28, 2, 26, 37, tzinfo=tzutc())

    # The Hobbit: The Desolation of Smaug (2013)
    assert ratings[('imdb', 'tt1170358')].title == 'The Hobbit: The Desolation of Smaug'
    assert ratings[('imdb', 'tt1170358')].year == 2013

    assert ratings[('imdb', 'tt1170358')].pk == ('imdb', 'tt1170358')
    assert ratings[('imdb', 'tt1170358')].keys == [
        ('imdb', 'tt1170358'),
        ('tmdb', '57158'),
        ('slug', 'the-hobbit-the-desolation-of-smaug-2013'),
        ('trakt', '40808')
    ]

    assert ratings[('imdb', 'tt1170358')].rating.value == 10
    assert ratings[('imdb', 'tt1170358')].rating.timestamp == datetime(2014, 11, 1, 0, 24, 54, tzinfo=tzutc())


@responses.activate
def test_watched():
    responses.add_callback(
        responses.GET, 'http://mock/sync/watched/movies',
        callback=authenticated_response('fixtures/sync/watched/movies.json'),
        content_type='application/json'
    )

    Trakt.base_url = 'http://mock'

    with Trakt.configuration.auth('mock', 'mock'):
        watched = Trakt['sync/watched'].movies()

    assert watched is not None

    # 100 Bloody Acres (2012)
    assert watched[('imdb', 'tt2290065')].title == '100 Bloody Acres'
    assert watched[('imdb', 'tt2290065')].year == 2012

    assert watched[('imdb', 'tt2290065')].pk == ('imdb', 'tt2290065')
    assert watched[('imdb', 'tt2290065')].keys == [
        ('imdb', 'tt2290065'),
        ('tmdb', '126757'),
        ('slug', '100-bloody-acres-2012'),
        ('trakt', '86920')
    ]

    assert watched[('imdb', 'tt2290065')].plays == 2
    assert watched[('imdb', 'tt2290065')].last_watched_at == datetime(2014, 4, 27, 13, 43, 59, tzinfo=tzutc())

    # The Hobbit: The Desolation of Smaug (2013)
    assert watched[('imdb', 'tt1170358')].title == 'The Hobbit: The Desolation of Smaug'
    assert watched[('imdb', 'tt1170358')].year == 2013

    assert watched[('imdb', 'tt1170358')].pk == ('imdb', 'tt1170358')
    assert watched[('imdb', 'tt1170358')].keys == [
        ('imdb', 'tt1170358'),
        ('tmdb', '57158'),
        ('slug', 'the-hobbit-the-desolation-of-smaug-2013'),
        ('trakt', '40808')
    ]

    assert watched[('imdb', 'tt1170358')].plays == 1
    assert watched[('imdb', 'tt1170358')].last_watched_at == datetime(2014, 4, 20, 12, 32, 59, tzinfo=tzutc())

    # TRON: Legacy (2010)
    assert watched[('imdb', 'tt1104001')].title == 'TRON: Legacy'
    assert watched[('imdb', 'tt1104001')].year == 2010

    assert watched[('imdb', 'tt1104001')].pk == ('imdb', 'tt1104001')
    assert watched[('imdb', 'tt1104001')].keys == [
        ('imdb', 'tt1104001'),
        ('tmdb', '20526'),
        ('slug', 'tron-legacy-2010'),
        ('trakt', '12601')
    ]

    assert watched[('imdb', 'tt1104001')].plays == 1
    assert watched[('imdb', 'tt1104001')].last_watched_at == datetime(2015, 1, 27, 23, 30, 16, tzinfo=tzutc())
