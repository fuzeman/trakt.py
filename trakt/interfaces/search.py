

from trakt.core.helpers import dictfilter
from trakt.core.pagination import PaginationIterator
from trakt.interfaces.base import Interface
from trakt.mapper.search import SearchMapper

import requests
import warnings


class SearchInterface(Interface):
    path = 'search'

    def lookup(self, id, service=None, media=None, extended=None, page=None, per_page=None, **kwargs):
        """Lookup items by their Trakt, IMDB, TMDB, TVDB, or TVRage ID.

        **Note:** If you lookup an identifier without a :code:`media` type specified it
        might return multiple items if the :code:`service` is not globally unique.

        :param id: Identifier value to lookup
        :type id: :class:`~python:str` or :class:`~python:int`

        :param service: Identifier service

            **Possible values:**
             - :code:`trakt`
             - :code:`imdb`
             - :code:`tmdb`
             - :code:`tvdb`
             - :code:`tvrage`

        :type service: :class:`~python:str`

        :param media: Desired media type (or :code:`None` to return all matching items)

            **Possible values:**
             - :code:`movie`
             - :code:`show`
             - :code:`episode`
             - :code:`person`
             - :code:`list`

        :type media: :class:`~python:str` or :class:`~python:list` of :class:`~python:str`

        :param extended: Level of information to include in response

            **Possible values:**
             - :code:`None`: Minimal (e.g. title, year, ids) **(default)**
             - :code:`full`: Complete

        :type extended: :class:`~python:str`

        :param kwargs: Extra request options
        :type kwargs: :class:`~python:dict`

        :return: Results
        :rtype: :class:`~python:list` of :class:`trakt.objects.media.Media`
        """
        # Expand tuple `id`
        if type(id) is tuple:
            if len(id) != 2:
                raise ValueError()

            id, service = id

        # Validate parameters
        if not service:
            raise ValueError('Invalid value provided for the "service" parameter')

        # Build query
        query = {
            'extended': extended,
            'page': page,
            'limit': per_page
        }

        if isinstance(media, str):
            query['type'] = media
        elif isinstance(media, list):
            query['type'] = ','.join(media)

        # Send request
        response = self.http.get(
            params=[service, id],
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
            return items.with_mapper(lambda items: SearchMapper.process_many(self.client, items))

        if isinstance(items, requests.Response):
            return items

        return SearchMapper.process_many(self.client, items)

    def query(self, query, media=None, year=None, fields=None, extended=None, page=None, per_page=None, **kwargs):
        """Search by titles, descriptions, translated titles, aliases, and people.

        **Note:** Results are ordered by the most relevant score.

        :param query: Search title or description
        :type query: :class:`~python:str`

        :param media: Desired media type (or :code:`None` to return all matching items)

            **Possible values:**
             - :code:`movie`
             - :code:`show`
             - :code:`episode`
             - :code:`person`
             - :code:`list`

        :type media: :class:`~python:str` or :class:`~python:list` of :class:`~python:str`

        :param year: Desired media year (or :code:`None` to return all matching items)
        :type year: :class:`~python:str` or :class:`~python:int`

        :param fields: Fields to search for :code:`query` (or :code:`None` to search all fields)
        :type fields: :class:`~python:str` or :class:`~python:list`

        :param extended: Level of information to include in response

            **Possible values:**
             - :code:`None`: Minimal (e.g. title, year, ids) **(default)**
             - :code:`full`: Complete

        :type extended: :class:`~python:str`

        :param kwargs: Extra request options
        :type kwargs: :class:`~python:dict`

        :return: Results
        :rtype: :class:`~python:list` of :class:`trakt.objects.media.Media`
        """
        # Validate parameters
        if not media:
            warnings.warn(
                "\"media\" parameter is now required on the Trakt['search'].query() method",
                DeprecationWarning, stacklevel=2
            )

        if fields and not media:
            raise ValueError('"fields" can only be used when the "media" parameter is defined')

        # Build query
        query = {
            'query': query,
            'year': year,
            'fields': fields,

            'extended': extended,
            'page': page,
            'limit': per_page
        }

        # Serialize media items
        if isinstance(media, list):
            media = ','.join(media)

        # Send request
        response = self.http.get(
            params=[media],
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
            return items.with_mapper(lambda items: SearchMapper.process_many(self.client, items))

        if isinstance(items, requests.Response):
            return items

        return SearchMapper.process_many(self.client, items)
