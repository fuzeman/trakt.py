from trakt.core.helpers import deprecated
from trakt.models.media.base import Media
from trakt.models.summary import SummaryItem

from byte.model import Property


class Episode(Media):
    class Options:
        slots = True

    media_type = 'episode'

    show = Property('Show')
    season = Property('Season')

    title = Property(str)

    number = Property(int)
    number_abs = Property(int, nullable=True)

    summary = Property(SummaryItem)

    #
    # Compatibility Properties
    #

    @property
    @deprecated('`Episode.pk` has been deprecated, use: `Episode.season.number`, `Episode.number`')
    def pk(self):
        if not self.season:
            return None

        return self.season.number, self.number
