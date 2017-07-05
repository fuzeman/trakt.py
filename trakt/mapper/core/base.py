from __future__ import absolute_import, division, print_function

from trakt.models.metadata import Movie, Show, Episode, Season, Person


class Mapper(object):
    models = {
        'movie': Movie,

        'show': Show,
        'season': Season,
        'episode': Episode,

        'person': Person
    }

    # TODO Support `client` value
    @classmethod
    def construct(cls, client, media_type, item, **kwargs):
        item = cls.collapse(media_type, item)

        # Find model for provided `media` type
        model = cls.models.get(media_type)

        if not model:
            raise NotImplementedError('Unsupported media type: %s' % (media_type,))

        # Parse `item` with `model`
        return model.from_plain(
            item,
            translate=True,
            **kwargs
        )

    @classmethod
    def collapse(cls, media_type, item):
        if media_type in item:
            item.update(item.pop(media_type))

        return item
