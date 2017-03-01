from trakt.core.helpers import popitems
from trakt.interfaces.calendars.base.movies import CalendarsMoviesBaseInterface


class CalendarsAllMoviesInterface(CalendarsMoviesBaseInterface):
    path = 'calendars/all/movies'
