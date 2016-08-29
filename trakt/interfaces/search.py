from trakt.interfaces.base import Interface
from trakt.mapper.search import SearchMapper

import six


class SearchInterface(Interface):
    path = 'search'

    def lookup(self, id, service=None, media=None, **kwargs):
        if type(id) is tuple:
            if len(id) != 2:
                raise ValueError()

            # Expand (<id>, <service>) identifier
            id, service = id

        # Build query
        query = {
            'id': id,
            'id_type': service
        }

        if isinstance(media, six.string_types):
            query['type'] = media
        elif isinstance(media, list):
            query['type'] = ','.join(media)

        # Send request
        response = self.http.get(query=query)

        # Parse response
        items = self.get_data(response, **kwargs)

        if not items:
            return None

        count = len(items)

        if count > 1:
            return [SearchMapper.process(self.client, item) for item in items]
        elif count == 1:
            return SearchMapper.process(self.client, items[0])

        return None

    def query(self, query, media=None, year=None, **kwargs):
        query = {
            'query': query
        }

        # Set optional parameters
        if isinstance(media, six.string_types):
            query['type'] = media
        elif isinstance(media, list):
            query['type'] = ','.join(media)

        if year:
            query['year'] = year

        # Send request
        response = self.http.get(query=query)

        # Parse response
        items = self.get_data(response, **kwargs)

        if items is not None:
            return [SearchMapper.process(self.client, item) for item in items]

        return None
