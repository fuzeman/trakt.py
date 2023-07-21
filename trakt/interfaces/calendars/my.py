
from trakt.interfaces.base import authenticated
from trakt.interfaces.calendars import CalendarsInterface


class MyCalendarsInterface(CalendarsInterface):
    path = 'calendars/my/*'

    @authenticated
    def get(self, media, collection=None, start_date=None, days=None, **kwargs):
        return super(MyCalendarsInterface, self).get(
            'my', media, collection,
            start_date=start_date,
            days=days,
            **kwargs
        )
