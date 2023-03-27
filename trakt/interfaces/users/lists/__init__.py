

from trakt.core.helpers import clean_username
from trakt.interfaces.base import Interface
from trakt.mapper import ListMapper

import requests

# Import child interfaces
from trakt.interfaces.users.lists.list_ import UsersListInterface  # noqa: I100

__all__ = (
    'UsersListsInterface',
    'UsersListInterface'
)


class UsersListsInterface(Interface):
    path = 'users/*/lists'

    def create(self, username, name, description=None, privacy='private', display_numbers=False,
               allow_comments=True, sort_by='rank', sort_how='asc', **kwargs):
        """Create a new list.

        :param username: Username (or :code:`me`)
        :type username: :class:`~python:str`

        :param name: Name
        :type name: :class:`~python:str`

        :param description: Description
        :type description: :class:`~python:str`

        :param privacy: Privacy (:code:`private`, :code:`friends`, or :code:`public`)
        :type description: :class:`~python:str`

        :param display_numbers: Flag indicating this list displays numbers
        :type description: :class:`~python:bool`

        :param allow_comments: Flag indicating this list allows comments
        :type description: :class:`~python:bool`

        :param sort_by: Sort By (:code:`rank`, :code:`added`, :code:`title`, :code:`released`,
                        :code:`runtime`, :code:`popularity`, :code:`percentage`, :code:`votes`,
                        :code:`my_rating`, :code:`random`, :code:`watched`, :code:`collected`)
        :type sort_by: :class:`~python:str`

        :param sort_how: Sort Direction (:code:`asc`, or :code:`desc`)
        :type sort_how: :class:`~python:str`

        :return: List
        :rtype: trakt.objects.CustomList
        """
        data = {
            'name': name,
            'description': description,

            'privacy': privacy,
            'allow_comments': allow_comments,
            'display_numbers': display_numbers,
            'sort_by': sort_by,
            'sort_how': sort_how
        }

        # Remove attributes with `None` values
        for key in list(data.keys()):
            if data[key] is not None:
                continue

            del data[key]

        # Send request
        response = self.http.post(
            '/users/%s/lists' % clean_username(username),
            data=data
        )

        # Parse response
        item = self.get_data(response, **kwargs)

        if isinstance(item, requests.Response):
            return item

        if not item:
            return None

        # Map item to list object
        return ListMapper.custom_list(
            self.client, item,
            username=username
        )

    def get(self, username, **kwargs):
        """Retrieve lists for user.

        :param username: Username (or :code:`me`)
        :type username: :class:`~python:str`

        :return: List
        :rtype: trakt.objects.CustomList
        """
        if kwargs.get('parse') is False:
            raise ValueError("Parse can't be disabled on this method")

        # Send request
        response = self.http.get(
            '/users/%s/lists' % clean_username(username),
        )

        # Parse response
        items = self.get_data(response, **kwargs)

        if not items:
            return

        # Map items to list objects
        for item in items:
            yield ListMapper.custom_list(
                self.client, item,
                username=username
            )
