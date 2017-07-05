from trakt.models.user import User

from byte.model import Model, Property
from byte.types import Dictionary
from datetime import datetime


class List(Model):
    ids = Property(Dictionary(str))
    user = Property(User)

    name = Property(str)
    description = Property(str)
    likes = Property(int)

    allow_comments = Property(bool)
    display_numbers = Property(bool)
    privacy = Property(str)

    comment_count = Property(int)
    item_count = Property(int)

    sort_by = Property(str)
    sort_how = Property(str)

    created_at = Property(datetime)
    updated_at = Property(datetime)
