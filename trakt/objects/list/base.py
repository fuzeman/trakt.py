from trakt.core.helpers import from_iso8601
from trakt.objects.core.helpers import update_attributes


class List(object):
    def __init__(self, client, keys):
        self._client = client

        self.keys = keys
        """
        :type: list of (str, str)

        Keys (for trakt, imdb, tvdb, etc..)
        """

        self.name = None
        """
        :type: str

        Name
        """

        self.description = None
        """
        :type: str

        Description
        """

        self.likes = None
        """
        :type: int

        Number of likes
        """

        self.allow_comments = None
        """
        :type: boolean

        Flag indicating this list allows comments
        """

        self.display_numbers = None
        """
        :type: boolean

        Flag indicating this list displays numbers
        """

        self.liked_at = None
        """
        :type: datetime

        Timestamp of when this list was liked
        """

        self.updated_at = None
        """
        :type: datetime

        Timestamp of when this list was last updated
        """

        self.comment_count = None
        """
        :type: int

        Number of comments
        """

        self.item_count = None
        """
        :type: int

        Number of items
        """

    @property
    def id(self):
        """Returns the list identifier

        :rtype: int
        """

        if self.pk is None:
            return None

        _, sid = self.pk

        return sid

    @property
    def pk(self):
        """Primary Key (unique identifier for the list)

        :return: :code:`("trakt", <id>)` or :code:`None` if no primary key is available
        :rtype: (str, str) or None
        """

        if not self.keys:
            return None

        return self.keys[0]

    def _update(self, info=None):
        if not info:
            return

        if 'liked_at' in info:
            self.liked_at = from_iso8601(info.get('liked_at'))

        if 'updated_at' in info:
            self.updated_at = from_iso8601(info.get('updated_at'))

        update_attributes(self, info, [
            'name',
            'description',
            'likes',

            'allow_comments',
            'display_numbers',

            'comment_count',
            'item_count'
        ])

    def __getstate__(self):
        state = self.__dict__

        if hasattr(self, '_client'):
            del state['_client']

        return state

    def __repr__(self):
        _, sid = self.pk

        return '<List %r (%s)>' % (self.name, sid)

    def __str__(self):
        return self.__repr__()
