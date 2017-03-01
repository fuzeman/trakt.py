from trakt.core.helpers import popitems
from trakt.interfaces.calendars.base.movies import CalendarsMoviesBaseInterface


class CalendarsAllDvdInterface(CalendarsMoviesBaseInterface):
    path = 'calendars/all/dvd'
