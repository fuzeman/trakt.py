from trakt.core.helpers import deprecated
from trakt.models.core.helpers import property_proxy
from trakt.models.metadata.base import Media, Search, Summary, Trending
from trakt.models.metadata.season import Season

from byte.model import Property
from byte.types import List


class Show(Media):
    class Options:
        slots = True

    media_type = 'show'

    seasons = Property(List(Season))

    title = Property(str)
    year = Property(int)

    summary = Property(Summary, name=[
        'overview',

        'available_translations',
        'genres',

        'airs',

        'aired_episodes',
        'episode_count',
        'status',

        'certification',
        'country',
        'language',
        'network',
        'runtime',

        'homepage',
        'trailer',

        'rating',
        'votes',

        'first_aired',
        'updated_at'
    ])

    search = Property(Search, name=[
        'score',
        'type'
    ])

    trending = Property(Trending, name=[
        'watchers'
    ])

    @property
    def primary_key(self):
        identifier = self.identifiers.get('tvdb')

        if not identifier:
            return None

        return identifier

    #
    # Summary
    #

    overview = property_proxy('summary.overview', deprecated=True)

    available_translations = property_proxy('summary.available_translations', deprecated=True)
    genres = property_proxy('summary.genres', deprecated=True)

    aired_episodes = property_proxy('summary.aired_episodes', deprecated=True)
    episode_count = property_proxy('summary.episode_count', deprecated=True)
    status = property_proxy('summary.status', deprecated=True)

    certification = property_proxy('summary.certification', deprecated=True)
    country = property_proxy('summary.country', deprecated=True)
    language = property_proxy('summary.language', deprecated=True)
    network = property_proxy('summary.network', deprecated=True)
    runtime = property_proxy('summary.runtime', deprecated=True)

    homepage = property_proxy('summary.homepage', deprecated=True)
    trailer = property_proxy('summary.trailer', deprecated=True)

    rating = property_proxy('summary.rating', deprecated=True)
    votes = property_proxy('summary.votes', deprecated=True)

    first_aired = property_proxy('summary.first_aired', deprecated=True)
    updated_at = property_proxy('summary.updated_at', deprecated=True)

    @property
    @deprecated('`Show.airs` has been deprecated, use: `Show.summary.airs`')
    def airs(self):
        if not self.summary or not self.summary.airs:
            return None

        return self.summary.airs.to_plain()

    #
    # Trending
    #

    watchers = property_proxy('trending.watchers', deprecated=True)
