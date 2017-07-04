from trakt.core.helpers import deprecated
from trakt.models.core.helpers import property_proxy
from trakt.models.summary import SummaryItem
from trakt.models.media.base import Media
from trakt.models.media.season import Season

from byte.model import Property
from byte.types import List


class Show(Media):
    class Options:
        slots = True

    media_type = 'show'

    seasons = Property(List(Season))

    title = Property(str)
    year = Property(int)

    summary = Property(SummaryItem)

    @property
    def primary_key(self):
        identifier = self.identifiers.get('tvdb')

        if not identifier:
            return None

        return identifier

    #
    # Compatibility Properties
    #

    overview = property_proxy('overview', ['summary'], deprecated=True)

    available_translations = property_proxy('available_translations', ['summary'], deprecated=True)
    genres = property_proxy('genres', ['summary'], deprecated=True)

    status = property_proxy('status', ['summary'], deprecated=True)

    aired_episodes = property_proxy('aired_episodes', ['summary'], deprecated=True)
    episode_count = property_proxy('episode_count', ['summary'], deprecated=True)

    certification = property_proxy('certification', ['summary'], deprecated=True)
    country = property_proxy('country', ['summary'], deprecated=True)
    language = property_proxy('language', ['summary'], deprecated=True)
    network = property_proxy('network', ['summary'], deprecated=True)
    runtime = property_proxy('runtime', ['summary'], deprecated=True)

    homepage = property_proxy('homepage', ['summary'], deprecated=True)
    trailer = property_proxy('trailer', ['summary'], deprecated=True)

    rating = property_proxy('rating', ['summary'], deprecated=True)
    votes = property_proxy('votes', ['summary'], deprecated=True)

    first_aired = property_proxy('first_aired', ['summary'], deprecated=True)
    updated_at = property_proxy('updated_at', ['summary'], deprecated=True)

    @property
    @deprecated('`Show.airs` has been deprecated, use: `Show.summary.airs`')
    def airs(self):
        if not self.summary or not self.summary.airs:
            return None

        return self.summary.airs.to_plain()
