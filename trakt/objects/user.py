from __future__ import absolute_import, division, print_function

from trakt.core.helpers import from_iso8601_datetime
from trakt.objects.core.helpers import update_attributes


class User(object):
    def __init__(self, client, keys):
        self._client = client

        self.keys = keys
        """
        :type: :class:`~python:list` of :class:`~python:tuple`

        Keys (for trakt, imdb, tvdb, etc..), defined as:

        ..code-block::

            [
                (<service>, <id>)
            ]

        """

        self.name = None
        """
        :type: :class:`~python:str`

        Name
        """

        self.username = None
        """
        :type: :class:`~python:str`

        Username
        """

        self.vip = None
        """
        :type: :class:`~python:bool`

        Is account VIP
        """

        self.vip_es = None

        self.private = None
        """
        :type: :class:`~python:bool`

        Is account private
        """

        self.followed_at = None
        """
        :type: :class:`~python:datetime.datetime`

        Timestamp of when this user was followed
        """

        self.friends_at = None

    @property
    def id(self):
        """Retrieve the usr identifier.

        :rtype: :class:`~python:int`
        """

        if self.pk is None:
            return None

        _, sid = self.pk

        return sid

    @property
    def pk(self):
        """Retrieve the primary key (unique identifier for the user).

        :return: :code:`("trakt", <id>)` or :code:`None` if no primary key is available
        :rtype: :class:`~python:tuple`
        """

        if not self.keys:
            return None

        return self.keys[0]

    def following(self):
        return self._client['users/*/following'].get(self.id)

    def _update(self, info=None):
        if not info:
            return

        if 'followed_at' in info:
            self.followed_at = from_iso8601_datetime(info.get('followed_at'))

        if 'friends_at' in info:
            self.friends_at = from_iso8601_datetime(info.get('friends_at'))

        update_attributes(self, info, [
            'username',
            'name',
            'private',
            'vip',
            'vip_es'
        ])

    @classmethod
    def _construct(cls, client, keys, info, **kwargs):
        if not info:
            return None

        u = cls(client, keys, **kwargs)
        u._update(info)
        return u

    def __repr__(self):
        return '<User %r (%s)>' % (self.name, self.id)
