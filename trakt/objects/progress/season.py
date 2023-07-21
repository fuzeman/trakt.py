
from trakt.objects.progress.base import BaseProgress
from trakt.objects.progress.episode import EpisodeProgress


class SeasonProgress(BaseProgress):
    def __init__(self, pk=None, aired=None, completed=None):
        super(SeasonProgress, self).__init__(aired, completed)

        self.pk = pk
        """
        :type: :class:`~python:int`

        Season Number
        """

        self.episodes = {}
        """
        :type: :class:`~python:dict`

        Episode Progress, defined as :code:`{episode_num: EpisodeProgress}`
        """

    def to_dict(self):
        result = super(SeasonProgress, self).to_dict()

        result['number'] = self.pk
        result['episodes'] = [
            episode.to_dict()
            for episode in self.episodes.values()
        ]
        return result

    def _update(self, info=None, **kwargs):
        if not info:
            return

        super(SeasonProgress, self)._update(info, **kwargs)

        self.pk = info['number']

        if 'episodes' in info:
            for episode in info['episodes']:
                episode_progress = EpisodeProgress._construct(episode, **kwargs)

                if episode_progress:
                    self.episodes[episode_progress.pk] = episode_progress

    @classmethod
    def _construct(cls, info=None, **kwargs):
        if not info:
            return

        season_progress = cls()
        season_progress._update(info, **kwargs)

        return season_progress
