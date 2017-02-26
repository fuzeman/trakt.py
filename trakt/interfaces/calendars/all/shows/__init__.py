from trakt.core.helpers import popitems
from trakt.interfaces.calendars.base.shows import CalendarsShowsBaseInterface


class CalendarsAllShowsInterface(CalendarsShowsBaseInterface):
    path = 'calendars/all/shows'
