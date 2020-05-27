from __future__ import absolute_import, division, print_function

from trakt.core.helpers import clean_username, dictfilter
from trakt.core.pagination import PaginationIterator
from trakt.interfaces.base import Interface
from trakt.mapper import ListItemMapper

import requests


class UsersHistoryInterface(Interface):
    path = 'users/*/history'

    def items(self, username, media=None, extended=None, page=None, per_page=None, **kwargs):
        print(kwargs)
        response = self.http.get(
            '/users/%s/history' % (clean_username(username)),
            query={
                'type': media,
                'extended': extended,
                'page': page,
                'limit': per_page
            },
            **dictfilter(kwargs, get=[
                'exceptions'
            ], pop=[
                'authenticated',
                'pagination',
                'validate_token'
            ])
        )
        items = self.get_data(response, **kwargs)

        if isinstance(items, PaginationIterator):
            return items.with_mapper(lambda items: ListItemMapper.process_many(self.client, items))

        if isinstance(items, requests.Response):
            return items

        return ListItemMapper.process_many(self.client, items)
