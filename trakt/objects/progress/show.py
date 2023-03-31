
from trakt.core.helpers import dictfilter, from_iso8601_datetime, to_iso8601_datetime
from trakt.objects.progress.base import BaseProgress
from trakt.objects.progress.season import SeasonProgress


LABELS = {
    'watched': 'last_watched_at',
    'collection': 'last_collected_at'
}

class ShowProgress(BaseProgress):
    progress_type = None
    """
    :type: :class:`~python:str`

    Progress Type (:code:`watched` or :code:`collection`)
    """

    def __init__(self, client, aired=None, completed=None):
        super(ShowProgress, self).__init__(aired, completed)

        self._client = client

        self.last_progress_change = None
        """
        :type: :class:`~python:datetime.datetime`

        Last watched or collected date/time
        """

        self.reset_at = None
        """
        :type: :class:`~python:datetime.datetime`

        Reset date/time (not applicable for collected progress)
        """

        self.seasons = {}
        """
        :type: :class:`~python:dict`

        Season Progress, defined as :code:`{season_num: SeasonProgress}`
        """

        self.hidden_seasons = None
        """
        :type: :class:`~python:dict`

        Hidden Seasons, defined as :code:`{season_num: Season}`
        """

        self.next_episode = None
        """
        :type: :class:`trakt.objects.episode.Episode`

        Next Episode the user should watch or collect
        """

        self.last_episode = None
        """
        :type: :class:`trakt.objects.episode.Episode`

        Last Episode the user watched or collected
        """

    def to_dict(self):
        """Dump progress to a dictionary.

        :return: Progress dictionary
        :rtype: :class:`~python:dict`
        """

        result = super(ShowProgress, self).to_dict()

        label = LABELS[self.progress_type]
        result[label] = to_iso8601_datetime(self.last_progress_change)

        if self.progress_type == 'watched':
            result['reset_at'] = self.reset_at

        result['seasons'] = [
            season.to_dict()
            for season in self.seasons.values()
        ]

        if self.hidden_seasons:
            result['hidden_seasons'] = [
                dictfilter(season.to_dict(), pop=['number', 'ids'])
                for season in self.hidden_seasons.values()
            ]

        if self.next_episode:
            result['next_episode'] = dictfilter(self.next_episode.to_dict(), pop=['season', 'number', 'title', 'ids'])
            result['next_episode']['season'] = self.next_episode.keys[0][0]

        if self.last_episode:
            result['last_episode'] = dictfilter(self.last_episode.to_dict(), pop=['season', 'number', 'title', 'ids'])
            result['last_episode']['season'] = self.last_episode.keys[0][0]

        return result

    def _update(self, info=None, **kwargs):
        if not info:
            return

        super(ShowProgress, self)._update(info, **kwargs)

        label = LABELS[self.progress_type]

        if label in info:
            self.last_progress_change = from_iso8601_datetime(info.get(label))

        if 'reset_at' in info:
            self.reset_at = from_iso8601_datetime(info.get('reset_at'))

        if 'seasons' in info:
            for season in info['seasons']:
                season_progress = SeasonProgress._construct(season, progress_type=self.progress_type)

                if season_progress:
                    self.seasons[season_progress.pk] = season_progress

        if 'hidden_seasons' in info:
            self.hidden_seasons = {}

            for season in info['hidden_seasons']:
                hidden_season = self._client.construct('season', season)

                if hidden_season:
                    self.hidden_seasons[hidden_season.pk] = hidden_season

        if 'next_episode' in info:
            episode = self._client.construct('episode', info['next_episode'])

            if episode:
                self.next_episode = episode

        if 'last_episode' in info:
            episode = self._client.construct('episode', info['last_episode'])

            if episode:
                self.last_episode = episode

    @classmethod
    def _construct(cls, client, info=None, **kwargs):
        if not info:
            return

        progress = cls(client)
        progress._update(info, **kwargs)

        return progress
