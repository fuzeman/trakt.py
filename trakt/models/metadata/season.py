from trakt.core.helpers import deprecated
from trakt.models.core.helpers import property_proxy
from trakt.models.metadata.base import Media, Summary
from trakt.models.metadata.episode import Episode

from byte.model import Property
from byte.types import Dictionary


class Season(Media):
    class Options:
        slots = True

    media_type = 'season'

    show = Property('Show')
    episodes = Property(Dictionary(Episode), exclude=True)

    title = Property(str)
    number = Property(int)

    summary = Property(Summary, name=[
        'overview',

        'aired_episodes',
        'episode_count',

        'rating',
        'votes',

        'first_aired'
    ])

    #
    # Summary
    #

    overview = property_proxy('summary.overview', deprecated=True)

    aired_episodes = property_proxy('summary.aired_episodes', deprecated=True)
    episode_count = property_proxy('summary.episode_count', deprecated=True)

    rating = property_proxy('summary.rating', deprecated=True)
    votes = property_proxy('summary.votes', deprecated=True)

    first_aired = property_proxy('summary.first_aired', deprecated=True)

    #
    # Season
    #

    @property
    @deprecated('`Season.keys` has been deprecated, use: `Season.identifiers`, `Season.ids`')
    def keys(self):
        return [self.pk] + super(Season, self).keys

    @property
    @deprecated('`Season.pk` has been deprecated, use: `Season.number`')
    def pk(self):
        return self.number
