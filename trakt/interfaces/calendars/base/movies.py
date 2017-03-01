from trakt.core.helpers import popitems
from trakt.interfaces.base import Interface, authenticated
from trakt.mapper.summary import SummaryMapper
from datetime import date

import requests

class CalendarsMoviesBaseInterface(Interface):
    @authenticated
    def get(self, start_date: date, days: int, **kwargs):
        params = ['{:%Y-%m-%d}'.format(start_date), days]

        response = self.http.get(
            params=params,
            **popitems(kwargs, [
                'authenticated',
                'validate_token'
            ])
        )

        items = self.get_data(response, **kwargs)

        if isinstance(items, requests.Response):
            return items

        return SummaryMapper.movies(self.client, items)
