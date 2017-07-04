from trakt.core.helpers import deprecated
from trakt.models.media.base import Media
from trakt.models.media.episode import Episode
from trakt.models.summary import SummaryItem

from byte.model import Property
from byte.types import List


class Season(Media):
    class Options:
        slots = True

    media_type = 'season'

    show = Property('Show')
    episodes = Property(List(Episode))

    title = Property(str)
    number = Property(int)

    summary = Property(SummaryItem)

    #
    # Compatibility Properties
    #

    @property
    @deprecated('`Season.keys` has been deprecated, use: `Season.identifiers`, `Season.ids`')
    def keys(self):
        return [self.number] + super(Season, self).keys

    @property
    @deprecated('`Season.pk` has been deprecated, use: `Season.number`')
    def pk(self):
        return self.number
