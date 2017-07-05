from __future__ import absolute_import, division, print_function

from trakt.interfaces.base import Interface
from trakt.mapper.basic import BasicMapper

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
        return BasicMapper.movie(self.client, items)

    def trending(self, extended=None, **kwargs):
        response = self.http.get('trending', query={
            'extended': extended
        })

        items = self.get_data(response, **kwargs)

        if isinstance(items, requests.Response):
            return items

        return BasicMapper.movies(self.client, items)
