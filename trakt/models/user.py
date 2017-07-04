from trakt.models.identifier import Identifier

from byte.model import Model, Property
from byte.types import Dictionary
from datetime import datetime


class User(Model):
    ids = Property(Dictionary(Identifier))

    username = Property(str)
    private = Property(bool)

    #
    # Extended
    #

    name = Property(str)

    about = Property(str)
    age = Property(int)
    gender = Property(str)
    location = Property(str)

    vip = Property(bool)
    vip_ep = Property(bool)

    images = Property(Dictionary(Dictionary(str)))

    joined_at = Property(datetime)
