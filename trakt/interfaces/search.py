from trakt.interfaces.base import Interface
from trakt.mapper.search import SearchMapper

import six


class SearchInterface(Interface):
    path = 'search'

    def lookup(self, id, service=None, media=None, **kwargs):
        """Lookup items by their Trakt, IMDB, TMDB, TVDB, or TVRage ID.

        **Note:** If you lookup an identifier without a :code:`media` type specified it
        might return multiple items if the :code:`service` is not globally unique.

        :param id: Identifier value to lookup
        :type id: str or int

        :param service: Identifier service

            **Possible values:**
             - :code:`trakt`
             - :code:`imdb`
             - :code:`tmdb`
             - :code:`tvdb`
             - :code:`tvrage`

        :type service: str

        :param media: Desired media type (or :code:`None` to return all matching items)

            **Possible values:**
             - :code:`movie`
             - :code:`show`
             - :code:`episode`
             - :code:`person`
             - :code:`list`

        :type media: str or list of str or None

        :param kwargs: Extra request options
        :type kwargs: dict

        :return: Results
        :rtype: Media or list of Media
        """
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
        """Search by titles, descriptions, translated titles, aliases, and people.

        **Note:** Results are ordered by the most relevant score.

        :param query: Search title or description
        :type query: str

        :param media: Desired media type (or :code:`None` to return all matching items)

            **Possible values:**
             - :code:`movie`
             - :code:`show`
             - :code:`episode`
             - :code:`person`
             - :code:`list`

        :type media: str or list of str or None

        :param year: Desired media year (or :code:`None` to return all matching items)
        :type year: str or int or None

        :param kwargs: Extra request options
        :type kwargs: dict

        :return: Results
        :rtype: list of Media
        """
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
