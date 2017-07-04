from trakt.core.helpers import deprecated
from trakt.models.core.helpers import property_proxy
from trakt.models.media.base import Media
from trakt.models.summary import SummaryItem

from byte.model import Property
from byte.types import Embedded


class Movie(Media):
    class Options:
        slots = True

    media_type = 'movie'

    title = Property(str)
    year = Property(int)

    summary = Property(Embedded(SummaryItem))

    @property
    def primary_key(self):
        identifier = self.identifiers.get('imdb')

        if not identifier:
            return None

        return identifier

    #
    # Compatibility Properties
    #

    overview = property_proxy('overview', ['summary'], deprecated=True)
    tagline = property_proxy('tagline', ['summary'], deprecated=True)

    available_translations = property_proxy('available_translations', ['summary'], deprecated=True)
    certification = property_proxy('certification', ['summary'], deprecated=True)
    genres = property_proxy('genres', ['summary'], deprecated=True)
    language = property_proxy('language', ['summary'], deprecated=True)
    runtime = property_proxy('runtime', ['summary'], deprecated=True)

    homepage = property_proxy('homepage', ['summary'], deprecated=True)
    trailer = property_proxy('trailer', ['summary'], deprecated=True)

    rating = property_proxy('rating', ['summary'], deprecated=True)
    votes = property_proxy('votes', ['summary'], deprecated=True)

    released = property_proxy('released', ['summary'], deprecated=True)
    updated_at = property_proxy('updated_at', ['summary'], deprecated=True)
