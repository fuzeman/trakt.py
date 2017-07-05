from trakt.core.helpers import deprecated
from trakt.models.core.helpers import property_proxy
from trakt.models.metadata.base.identifier import Identifier
from trakt.models.metadata.core.helpers import build_keys

from byte.model import Model, Property
from byte.types import Dictionary
import six


class Media(Model):
    class Options:
        slots = True

    media_type = None

    identifiers = Property(Dictionary(Identifier), name='ids')

    @property
    def id(self):
        identifier = self.identifiers.get('trakt')

        if not identifier:
            return None

        return identifier.value

    @property
    def ids(self):
        return dict([
            (name, identifier.value)
            for name, identifier in six.iteritems(self.identifiers)
            if identifier is not None
        ])

    #
    # Compatibility Properties
    #

    score = property_proxy('search.score', deprecated=True)
    type = property_proxy('search.type', deprecated=True)

    @property
    @deprecated('`Media.keys` has been deprecated, use: `Media.identifiers`, `Media.ids`')
    def keys(self):
        if self.media_type is None:
            raise ValueError('\'%s.media_type\' hasn\'t been defined' % (self.__class__.__name__,))

        return build_keys(self.media_type, self.ids)

    @property
    @deprecated('`Media.pk` has been deprecated, use: `Media.identifiers`, `Media.ids`, `Media.id`')
    def pk(self):
        keys = self.keys

        if not keys:
            return None

        return keys[0]
