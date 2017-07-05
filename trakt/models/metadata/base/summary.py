from trakt.models.metadata.base.airs import Airs

from byte.model import Model, Property
from byte.types import List
from datetime import date, datetime


class Summary(Model):
    overview = Property(str)
    tagline = Property(str, nullable=True)

    available_translations = Property(List(str))
    genres = Property(List(str))

    certification = Property(str)
    language = Property(str)
    runtime = Property(int)

    homepage = Property(str, nullable=True)
    trailer = Property(str, nullable=True)

    rating = Property(float)
    votes = Property(int)

    updated_at = Property(datetime)

    #
    # Movie
    #

    released = Property(date, nullable=True)

    #
    # Television
    #

    airs = Property(Airs, nullable=True)

    aired_episodes = Property(int, nullable=True)
    episode_count = Property(int)
    status = Property(str, nullable=True)

    country = Property(str, nullable=True)
    network = Property(str, nullable=True)

    first_aired = Property(datetime, nullable=True)
