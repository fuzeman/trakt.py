from trakt.core.helpers import popitems
from trakt.interfaces.calendars.base.shows import CalendarsShowsBaseInterface


class CalendarsMyShowsInterface(CalendarsShowsBaseInterface):
    path = 'calendars/my/shows'
