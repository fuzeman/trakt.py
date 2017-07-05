from trakt.core.helpers import deprecated
from trakt.models.core.helpers import property_proxy
from trakt.models.metadata.base import Media, Search, Summary

from byte.model import Property


class Episode(Media):
    class Options:
        slots = True

    media_type = 'episode'

    show = Property('Show')
    season = Property('Season', exclude=True)

    title = Property(str)

    number = Property(int)
    number_abs = Property(int, nullable=True)

    _season_number = Property(int, name='season', nullable=True)

    summary = Property(Summary, name=[
        'overview',

        'available_translations',
        'runtime',

        'rating',
        'votes',

        'first_aired',
        'updated_at'
    ])

    search = Property(Search, name=[
        'score',
        'type'
    ])

    @property
    def season_number(self):
        if self.season:
            return self.season.number

        return self._season_number

    #
    # Summary
    #

    overview = property_proxy('summary.overview', deprecated=True)

    available_translations = property_proxy('summary.available_translations', deprecated=True)
    runtime = property_proxy('summary.runtime', deprecated=True)

    rating = property_proxy('summary.rating', deprecated=True)
    votes = property_proxy('summary.votes', deprecated=True)

    first_aired = property_proxy('summary.first_aired', deprecated=True)
    updated_at = property_proxy('summary.updated_at', deprecated=True)

    #
    # Episode
    #

    @property
    @deprecated('`Episode.keys` has been deprecated, use: `Episode.identifiers`, `Episode.ids`')
    def keys(self):
        return [self.pk] + super(Episode, self).keys

    @property
    @deprecated('`Episode.pk` has been deprecated, use: `Episode.season.number`, `Episode.number`')
    def pk(self):
        return self.season_number, self.number
