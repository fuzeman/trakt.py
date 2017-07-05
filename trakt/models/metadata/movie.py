from trakt.models.core.helpers import property_proxy
from trakt.models.metadata.base import Media, Search, Summary, Trending

from byte.model import Property


class Movie(Media):
    class Options:
        slots = True

    media_type = 'movie'

    title = Property(str)
    year = Property(int)

    summary = Property(Summary, name=[
        'overview',
        'tagline',

        'available_translations',
        'genres',

        'certification',
        'language',
        'runtime',

        'homepage',
        'trailer',

        'rating',
        'votes',

        'released',
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
        identifier = self.identifiers.get('imdb')

        if not identifier:
            return None

        return identifier

    #
    # Summary
    #

    overview = property_proxy('summary.overview', deprecated=True)
    tagline = property_proxy('summary.tagline', deprecated=True)

    available_translations = property_proxy('summary.available_translations', deprecated=True)
    certification = property_proxy('summary.certification', deprecated=True)
    genres = property_proxy('summary.genres', deprecated=True)
    language = property_proxy('summary.language', deprecated=True)
    runtime = property_proxy('summary.runtime', deprecated=True)

    homepage = property_proxy('summary.homepage', deprecated=True)
    trailer = property_proxy('summary.trailer', deprecated=True)

    rating = property_proxy('summary.rating', deprecated=True)
    votes = property_proxy('summary.votes', deprecated=True)

    released = property_proxy('summary.released', deprecated=True)
    updated_at = property_proxy('summary.updated_at', deprecated=True)

    watchers = property_proxy('trending.watchers', deprecated=True)
