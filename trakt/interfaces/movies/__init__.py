from __future__ import absolute_import, division, print_function

from trakt.core.helpers import dictfilter
from trakt.core.pagination import PaginationIterator
from trakt.interfaces.base import Interface
from trakt.mapper.summary import SummaryMapper

import requests


class MoviesInterface(Interface):
    path = 'movies'

    def get(self, id, extended=None, **kwargs):
        response = self.http.get(str(id), query={
            'extended': extended
        })

        items = self.get_data(response, **kwargs)

        if isinstance(items, requests.Response):
            return items

        # Parse response
        return SummaryMapper.movie(self.client, items)

    def trending(self, extended=None, page=None, per_page=None, **kwargs):
        return self.parse_list('trending', extended=extended, page=page, per_page=per_page, **kwargs)

    def popular(self, extended=None, page=None, per_page=None, **kwargs):
        return self.parse_list('popular', extended=extended, page=page, per_page=per_page, **kwargs)

    def recommended(self, period=None, extended=None, page=None, per_page=None, **kwargs):
        return self.parse_list('recommended', period=period, extended=extended, page=page, per_page=per_page, **kwargs)

    def played(self, period=None, extended=None, page=None, per_page=None, **kwargs):
        return self.parse_list('played', period=period, extended=extended, page=page, per_page=per_page, **kwargs)

    def watched(self, period=None, extended=None, page=None, per_page=None, **kwargs):
        return self.parse_list('watched', period=period, extended=extended, page=page, per_page=per_page, **kwargs)

    def collected(self, period=None, extended=None, page=None, per_page=None, **kwargs):
        return self.parse_list('collected', period=period, extended=extended, page=page, per_page=per_page, **kwargs)

    def parse_list(self, list_type, period=None, extended=None, page=None, per_page=None, **kwargs):
        # Build parameters
        params = [period] if period else None

        # Build query
        query = {
            'extended': extended,
            'page': page,
            'limit': per_page
        }

        # Send request
        response = self.http.get(
            list_type,
            params=params,
            query=query,
            **dictfilter(kwargs, get=[
                'exceptions'
            ], pop=[
                'pagination'
            ])
        )

        # Parse response
        items = self.get_data(response, **kwargs)

        if isinstance(items, PaginationIterator):
            return items.with_mapper(lambda items: SummaryMapper.movies(self.client, items))

        if isinstance(items, requests.Response):
            return items

        return SummaryMapper.movies(self.client, items)
