
from trakt.objects.core.helpers import update_attributes


class BaseProgress(object):
    def __init__(self, aired=None, completed=None):
        self.aired = aired
        """
        :type: :class:`~python:int`

        Number of aired episodes
        """

        self.completed = completed
        """
        :type: :class:`~python:int`

        Number of completed episodes
        """

    def to_dict(self):
        return {
            'aired': self.aired,
            'completed': self.completed
        }

    def _update(self, info=None, **kwargs):
        if not info:
            return

        update_attributes(self, info, [
            'aired',
            'completed'
        ])

    def __repr__(self):
        return f'{self.completed}/{self.aired} episodes completed'