from trakt.core.helpers import from_iso8601
from trakt.objects.core.helpers import update_attributes


class Comment(object):
    def __init__(self, client, keys):
        self._client = client

        self.keys = keys
        """
        :type: list of (str, str)

        Keys (for trakt, imdb, tvdb, etc..)
        """

        self.parent_id = None
        """
        :type: int

        Parent comment id
        """

        self.comment = None
        """
        :type: str

        Comment body
        """

        self.spoiler = None
        """
        :type: boolean

        Flag indicating this comment has a spoiler
        """

        self.review = None
        """
        :type: boolean

        Flag indicating this comment is a review
        """

        self.replies = None
        """
        :type: int

        Number of replies
        """

        self.likes = None
        """
        :type: int

        Number of likes
        """

        self.created_at = None
        """
        :type: datetime

        Timestamp of when this comment was created
        """

        self.liked_at = None
        """
        :type: datetime

        Timestamp of when this comment was liked
        """

        self.user = None
        """
        :type: dict

        Author details
        """

        self.user_rating = None
        """
        :type: float

        Author rating for the item
        """

    @property
    def id(self):
        """Returns the comment identifier

        :rtype: int
        """

        if self.pk is None:
            return None

        _, sid = self.pk

        return sid

    @property
    def pk(self):
        """Primary Key (unique identifier for the comment)

        :return: :code:`("trakt", <id>)` or :code:`None` if no primary key is available
        :rtype: (str, str) or None
        """

        if not self.keys:
            return None

        return self.keys[0]

    def _update(self, info=None):
        if not info:
            return

        if 'created_at' in info:
            self.created_at = from_iso8601(info.get('created_at'))

        if 'liked_at' in info:
            self.liked_at = from_iso8601(info.get('liked_at'))

        update_attributes(self, info, [
            'parent_id',

            'comment',

            'spoiler',
            'review',

            'replies',
            'likes',

            'user',
            'user_rating'
        ])

    @classmethod
    def _construct(cls, client, keys, info, **kwargs):
        if not info:
            return None

        c = cls(client, keys, **kwargs)
        c._update(info)
        return c

    def __repr__(self):
        return '<Comment %r (%s)>' % (self.comment, self.id)

    def __str__(self):
        return self.__repr__()
