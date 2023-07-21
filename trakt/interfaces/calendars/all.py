
from trakt.interfaces.calendars.base import CalendarsInterface


class AllCalendarsInterface(CalendarsInterface):
    path = 'calendars/all/*'

    def get(self, media, collection=None, start_date=None, days=None, **kwargs):
        return super(AllCalendarsInterface, self).get(
            'all', media, collection,
            start_date=start_date,
            days=days,
            **kwargs
        )
