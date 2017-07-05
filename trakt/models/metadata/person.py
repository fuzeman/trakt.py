from trakt.models.metadata.base import Media

from byte.model import Property
from datetime import date


class Person(Media):
    class Options:
        slots = True

    name = Property(str)

    #
    # Extended
    #

    biography = Property(str)
    birthplace = Property(str)
    homepage = Property(str)

    birthday = Property(date)
    death = Property(date)
