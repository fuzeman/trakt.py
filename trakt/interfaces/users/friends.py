from __future__ import absolute_import, division, print_function

from trakt.core.helpers import clean_username
from trakt.interfaces.base import Interface
from trakt.mapper import UserMapper


class UsersFriendsInterface(Interface):
    path = 'users/*/friends'

    def get(self, username, extended=None, **kwargs):
        # Send request
        response = self.http.get(
            '/users/%s/friends' % (clean_username(username))
        )

        items = self.get_data(response, **kwargs)
        if not items:
            return

        for item in items:
            yield UserMapper.user(
                self.client, item
            )
