
from trakt.core.helpers import from_iso8601_datetime, to_iso8601_datetime


LABELS = {
    'watched': 'last_watched_at',
    'collection': 'collected_at'
}


class EpisodeProgress(object):
    def __init__(self, pk=None):
        self.progress_type = None

        self.pk = pk
        """
        :type: :class:`~python:int`

        Episode Number
        """

        self.completed = None
        """
        :type: :class:`~python:bool`

        Whether or not the episode has been watched or collected
        """

        self.progress_timestamp = None
        """
        :type: :class:`~python:datetime.datetime`

        Date/time episode was collected or last watched
        """

    def to_dict(self):
        result = {
            'number': self.pk,
            'completed': self.completed if self.completed is not None else 0
        }

        if self.progress_type:
            label = LABELS[self.progress_type]
        else:
            label = 'progress_timestamp'

        result[label] = to_iso8601_datetime(self.progress_timestamp)

        return result

    def _update(self, info=None, **kwargs):
        if not info:
            return

        self.pk = info['number']

        if 'progress_type' in kwargs:
            self.progress_type = kwargs['progress_type']

        self.completed = info['completed']

        if 'last_watched_at' in info:
            self.progress_timestamp = from_iso8601_datetime(info.get('last_watched_at'))

        elif 'collected_at' in info:
            self.progress_timestamp = from_iso8601_datetime(info.get('collected_at'))

    @classmethod
    def _construct(cls, info=None, **kwargs):
        if not info:
            return

        episode_progress = cls()
        episode_progress._update(info, **kwargs)

        return episode_progress