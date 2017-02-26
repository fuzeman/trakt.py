from trakt.core.helpers import popitems
from trakt.interfaces.calendars.base.movies import CalendarsMoviesBaseInterface


class CalendarsMyDvdInterface(CalendarsMoviesBaseInterface):
    path = 'calendars/my/dvd'
