# flake8: noqa: F403, F405
from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt
from trakt.interfaces.calendars import Base

from datetime import date, datetime
from dateutil.tz import tzutc
from hamcrest import *
from httmock import HTTMock
import pytest


def test_all_dvd():
    with HTTMock(mock.fixtures, mock.unknown):
        items = Trakt['calendars/all/dvd'].get()

    # Ensure request was successful
    assert_that(items, not_none())
    assert_that(items, has_length(3))

    # Guardians of the Galaxy (2014)
    assert_that(items[0], has_properties({
        'pk': ('imdb', 'tt2015381'),
        'title': u'Guardians of the Galaxy',
        'year': 2014,

        'released': date(2014, 8, 1)
    }))

    # Get On Up (2014)
    assert_that(items[1], has_properties({
        'pk': ('imdb', 'tt2473602'),
        'title': u'Get On Up',
        'year': 2014,

        'released': date(2014, 8, 1)
    }))

    # Teenage Mutant Ninja Turtles (2014)
    assert_that(items[2], has_properties({
        'pk': ('imdb', 'tt1291150'),
        'title': u'Teenage Mutant Ninja Turtles',
        'year': 2014,

        'released': date(2014, 8, 8)
    }))


def test_all_movies():
    with HTTMock(mock.fixtures, mock.unknown):
        items = Trakt['calendars/all/movies'].get()

    # Ensure request was successful
    assert_that(items, not_none())
    assert_that(items, has_length(3))

    # Guardians of the Galaxy (2014)
    assert_that(items[0], has_properties({
        'pk': ('imdb', 'tt2015381'),
        'title': u'Guardians of the Galaxy',
        'year': 2014,

        'released': date(2014, 8, 1)
    }))

    # Get On Up (2014)
    assert_that(items[1], has_properties({
        'pk': ('imdb', 'tt2473602'),
        'title': u'Get On Up',
        'year': 2014,

        'released': date(2014, 8, 1)
    }))

    # Teenage Mutant Ninja Turtles (2014)
    assert_that(items[2], has_properties({
        'pk': ('imdb', 'tt1291150'),
        'title': u'Teenage Mutant Ninja Turtles',
        'year': 2014,

        'released': date(2014, 8, 8)
    }))


def test_all_shows():
    with HTTMock(mock.fixtures, mock.unknown):
        items = Trakt['calendars/all/shows'].get()

    # Ensure request was successful
    assert_that(items, not_none())
    assert_that(items, has_length(4))

    # True Blood S07E04
    assert_that(items[0], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '82283'),
            'title': 'True Blood',
            'year': 2008
        }),

        'pk': (7, 4),
        'first_aired': datetime(2014, 7, 14, 1, tzinfo=tzutc())
    }))

    # The Leftovers S01E03
    assert_that(items[1], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '269689'),
            'title': 'The Leftovers',
            'year': 2014
        }),

        'pk': (1, 3),
        'first_aired': datetime(2014, 7, 14, 2, tzinfo=tzutc())
    }))

    # True Blood S07E05
    assert_that(items[2], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '82283'),
            'title': 'True Blood',
            'year': 2008
        }),

        'pk': (7, 5),
        'first_aired': datetime(2014, 7, 21, 1, tzinfo=tzutc())
    }))

    # The Leftovers S01E04
    assert_that(items[3], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '269689'),
            'title': 'The Leftovers',
            'year': 2014
        }),

        'pk': (1, 4),
        'first_aired': datetime(2014, 7, 21, 2, tzinfo=tzutc())
    }))


def test_all_shows_new():
    with HTTMock(mock.fixtures, mock.unknown):
        items = Trakt['calendars/all/shows'].new()

    # Ensure request was successful
    assert_that(items, not_none())
    assert_that(items, has_length(1))

    # True Blood S07E04
    assert_that(items[0], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '269689'),
            'title': 'The Leftovers',
            'year': 2014
        }),

        'pk': (1, 1),
        'first_aired': datetime(2014, 6, 30, 2, tzinfo=tzutc())
    }))


def test_all_shows_premieres():
    with HTTMock(mock.fixtures, mock.unknown):
        items = Trakt['calendars/all/shows'].premieres()

    # Ensure request was successful
    assert_that(items, not_none())
    assert_that(items, has_length(2))

    # The Leftovers S01E01
    assert_that(items[0], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '269689'),
            'title': 'The Leftovers',
            'year': 2014
        }),

        'pk': (1, 1),
        'first_aired': datetime(2014, 6, 30, 2, tzinfo=tzutc())
    }))

    # The Walking Dead S05E01
    assert_that(items[1], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '153021'),
            'title': 'The Walking Dead',
            'year': 2010
        }),

        'pk': (5, 1),
        'first_aired': datetime(2014, 10, 13, 1, tzinfo=tzutc())
    }))


def test_my_dvd():
    with HTTMock(mock.calendars_my, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['calendars/my/dvd'].get()

    # Ensure request was successful
    assert_that(items, not_none())
    assert_that(items, has_length(3))

    # Guardians of the Galaxy (2014)
    assert_that(items[0], has_properties({
        'pk': ('imdb', 'tt2015381'),
        'title': u'Guardians of the Galaxy',
        'year': 2014,

        'released': date(2014, 8, 1)
    }))

    # Get On Up (2014)
    assert_that(items[1], has_properties({
        'pk': ('imdb', 'tt2473602'),
        'title': u'Get On Up',
        'year': 2014,

        'released': date(2014, 8, 1)
    }))

    # Teenage Mutant Ninja Turtles (2014)
    assert_that(items[2], has_properties({
        'pk': ('imdb', 'tt1291150'),
        'title': u'Teenage Mutant Ninja Turtles',
        'year': 2014,

        'released': date(2014, 8, 8)
    }))


def test_my_movies():
    with HTTMock(mock.calendars_my, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['calendars/my/movies'].get()

    # Ensure request was successful
    assert_that(items, not_none())
    assert_that(items, has_length(3))

    # Guardians of the Galaxy (2014)
    assert_that(items[0], has_properties({
        'pk': ('imdb', 'tt2015381'),
        'title': u'Guardians of the Galaxy',
        'year': 2014,

        'released': date(2014, 8, 1)
    }))

    # Get On Up (2014)
    assert_that(items[1], has_properties({
        'pk': ('imdb', 'tt2473602'),
        'title': u'Get On Up',
        'year': 2014,

        'released': date(2014, 8, 1)
    }))

    # Teenage Mutant Ninja Turtles (2014)
    assert_that(items[2], has_properties({
        'pk': ('imdb', 'tt1291150'),
        'title': u'Teenage Mutant Ninja Turtles',
        'year': 2014,

        'released': date(2014, 8, 8)
    }))


def test_my_shows():
    with HTTMock(mock.calendars_my, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['calendars/my/shows'].get()

    # Ensure request was successful
    assert_that(items, not_none())
    assert_that(items, has_length(4))

    # True Blood S07E04
    assert_that(items[0], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '82283'),
            'title': 'True Blood',
            'year': 2008
        }),

        'pk': (7, 4),
        'first_aired': datetime(2014, 7, 14, 1, tzinfo=tzutc())
    }))

    # The Leftovers S01E03
    assert_that(items[1], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '269689'),
            'title': 'The Leftovers',
            'year': 2014
        }),

        'pk': (1, 3),
        'first_aired': datetime(2014, 7, 14, 2, tzinfo=tzutc())
    }))

    # True Blood S07E05
    assert_that(items[2], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '82283'),
            'title': 'True Blood',
            'year': 2008
        }),

        'pk': (7, 5),
        'first_aired': datetime(2014, 7, 21, 1, tzinfo=tzutc())
    }))

    # The Leftovers S01E04
    assert_that(items[3], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '269689'),
            'title': 'The Leftovers',
            'year': 2014
        }),

        'pk': (1, 4),
        'first_aired': datetime(2014, 7, 21, 2, tzinfo=tzutc())
    }))


def test_my_shows_new():
    with HTTMock(mock.calendars_my, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['calendars/my/shows'].new()

    # Ensure request was successful
    assert_that(items, not_none())
    assert_that(items, has_length(1))

    # True Blood S07E04
    assert_that(items[0], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '269689'),
            'title': 'The Leftovers',
            'year': 2014
        }),

        'pk': (1, 1),
        'first_aired': datetime(2014, 6, 30, 2, tzinfo=tzutc())
    }))


def test_my_shows_premieres():
    with HTTMock(mock.calendars_my, mock.unknown):
        with Trakt.configuration.auth('mock', 'mock'):
            items = Trakt['calendars/my/shows'].premieres()

    # Ensure request was successful
    assert_that(items, not_none())
    assert_that(items, has_length(2))

    # The Leftovers S01E01
    assert_that(items[0], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '269689'),
            'title': 'The Leftovers',
            'year': 2014
        }),

        'pk': (1, 1),
        'first_aired': datetime(2014, 6, 30, 2, tzinfo=tzutc())
    }))

    # The Walking Dead S05E01
    assert_that(items[1], has_properties({
        'show': has_properties({
            'pk': ('tvdb', '153021'),
            'title': 'The Walking Dead',
            'year': 2010
        }),

        'pk': (5, 1),
        'first_aired': datetime(2014, 10, 13, 1, tzinfo=tzutc())
    }))


def test_new_validation():
    with HTTMock(mock.fixtures, mock.unknown):
        with pytest.raises(ValueError):
            Trakt['calendars/all/dvd'].new()

        with pytest.raises(ValueError):
            Trakt['calendars/all/movies'].new()


def test_premieres_validation():
    with HTTMock(mock.fixtures, mock.unknown):
        with pytest.raises(ValueError):
            Trakt['calendars/all/dvd'].premieres()

        with pytest.raises(ValueError):
            Trakt['calendars/all/movies'].premieres()


def test_get_validation():
    with HTTMock(mock.fixtures, mock.unknown):
        with pytest.raises(ValueError):
            Base(None).get('invalid', 'movies')

        with pytest.raises(ValueError):
            Base(None).get('all', 'invalid')


def test_start_date():
    with HTTMock(mock.calendars_all_period, mock.unknown):
        items = Trakt['calendars/all/movies'].get(start_date=datetime(2015, 10, 15))

    assert_that(items, not_none())


def test_days():
    with HTTMock(mock.calendars_all_period, mock.unknown):
        items = Trakt['calendars/all/movies'].get(days=14)

    assert_that(items, not_none())
