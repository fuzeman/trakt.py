from __future__ import absolute_import, division, print_function

from trakt.core.helpers import clean_username, dictfilter
from trakt.core.pagination import PaginationIterator
from trakt.interfaces.base import Interface, authenticated
from trakt.mapper import ListMapper

import requests

class ListsInterface(Interface):
    path = 'lists'

    def popular(self, page=None, per_page=None, **kwargs):
        #Send response
        response = self.http.get('popular', query={
            'page': page,
            'limit': per_page
        }, **dictfilter(kwargs, get=[
            'exceptions'
        ], pop=[
            'pagination'
        ]))

        # Parse response
        items = self.get_data(response, **kwargs)

        if isinstance(items, PaginationIterator):
            return items.with_mapper(lambda items: ListMapper.lists(self.client, items))

        if isinstance(items, requests.Response):
            return items

        return ListMapper.lists(self.client, items)