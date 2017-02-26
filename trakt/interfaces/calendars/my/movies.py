from trakt.core.helpers import popitems
from trakt.interfaces.calendars.base.movies import CalendarsMoviesBaseInterface


class CalendarsMyMoviesInterface(CalendarsMoviesBaseInterface):
    path = 'calendars/my/movies'
