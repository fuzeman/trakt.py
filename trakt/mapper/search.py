from __future__ import absolute_import, division, print_function

from trakt.mapper.core.base import Mapper

import logging

log = logging.getLogger(__name__)


class SearchMapper(Mapper):
    @classmethod
    def process(cls, client, item, media=None, **kwargs):
        if media is None:
            # Retrieve `media` from `item`
            media = item.get('type')

        if not media:
            log.warn('Item %r has no "type" defined', media)
            return None

        # Find function for `media`
        func = getattr(cls, media, None)

        if not func:
            log.warn('Unknown media type: %r', media)
            return None

        # Map item
        return func(client, item, **kwargs)

    @classmethod
    def process_many(cls, client, items, **kwargs):
        result = []

        for item in items:
            item = cls.process(client, item, **kwargs)

            if not item:
                continue

            result.append(item)

        return result

    @classmethod
    def movie(cls, client, item, **kwargs):
        if not item:
            return None

        return cls.construct(client, 'movie', item, **kwargs)

    @classmethod
    def list(cls, client, item, **kwargs):
        if not item:
            return None

        return cls.construct(client, 'custom_list', item, **kwargs)

    @classmethod
    def officiallist(cls, client, item, **kwargs):
        return None

    @classmethod
    def person(cls, client, item, **kwargs):
        if not item:
            return None

        return cls.construct(client, 'person', item, **kwargs)

    @classmethod
    def show(cls, client, item, **kwargs):
        if not item:
            return None

        return cls.construct(client, 'show', item, **kwargs)

    @classmethod
    def episodes(cls, client, items, **kwargs):
        return [cls.episode(client, item, **kwargs) for item in items]

    @classmethod
    def episode(cls, client, item, **kwargs):
        if not item:
            return None

        episode = cls.construct(client, 'episode', item, **kwargs)

        if 'show' in item:
            episode.show = cls.show(client, item['show'])

        return episode
