# Import child interfaces
from trakt.interfaces.calendars.my.shows import CalendarsMyShowsInterface
from trakt.interfaces.calendars.my.shows.new import CalendarsMyShowsNewInterface
from trakt.interfaces.calendars.my.shows.premieres import CalendarsMyShowsPremieresInterface
from trakt.interfaces.calendars.my.movies import CalendarsMyMoviesInterface
from trakt.interfaces.calendars.my.dvd import CalendarsMyDvdInterface

from trakt.interfaces.calendars.all.shows import CalendarsAllShowsInterface
from trakt.interfaces.calendars.all.shows.new import CalendarsAllShowsNewInterface
from trakt.interfaces.calendars.all.shows.premieres import CalendarsAllShowsPremieresInterface
from trakt.interfaces.calendars.all.movies import CalendarsAllMoviesInterface
from trakt.interfaces.calendars.all.dvd import CalendarsAllDvdInterface

__all__ = [
    'CalendarsMyShowsInterface',
    'CalendarsMyShowsNewInterface',
    'CalendarsMyShowsPremieresInterface',
    'CalendarsMyMoviesInterface',
    'CalendarsMyDvdInterface',

    'CalendarsAllShowsInterface',
    'CalendarsAllShowsNewInterface',
    'CalendarsAllShowsPremieresInterface',
    'CalendarsAllMoviesInterface',
    'CalendarsAllDvdInterface',
]
