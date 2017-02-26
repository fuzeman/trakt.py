from trakt.core.helpers import popitems
from trakt.interfaces.calendars.base.shows import CalendarsShowsBaseInterface


class CalendarsAllShowsPremieresInterface(CalendarsShowsBaseInterface):
    path = 'calendars/all/shows/premieres'
