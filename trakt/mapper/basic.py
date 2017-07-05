from __future__ import absolute_import, division, print_function

from trakt.mapper.core.base import Mapper

import logging

log = logging.getLogger(__name__)


class BasicMapper(Mapper):
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
    def movies(cls, client, items, **kwargs):
        if not items:
            return None

        return [cls.movie(client, item, **kwargs) for item in items]

    @classmethod
    def movie(cls, client, item, **kwargs):
        if not item:
            return None

        return cls.construct(client, 'movie', item, **kwargs)

    @classmethod
    def shows(cls, client, items, **kwargs):
        if not items:
            return None

        return [cls.show(client, item, **kwargs) for item in items]

    @classmethod
    def show(cls, client, item, **kwargs):
        if not item:
            return None

        return cls.construct(client, 'show', item, **kwargs)

    @classmethod
    def seasons(cls, client, items, **kwargs):
        if not items:
            return None

        return [cls.season(client, item, **kwargs) for item in items]

    @classmethod
    def season(cls, client, item, **kwargs):
        if not item:
            return None

        episodes = item.pop('episodes', [])

        # Construct season
        season = cls.construct(client, 'season', item, **kwargs)

        # Construct episodes
        for i_episode in episodes:
            cls.season_episode(client, season, i_episode, **kwargs)

        return season

    @classmethod
    def season_episode(cls, client, season, item=None, **kwargs):
        if not item:
            return

        # Construct episode
        episode = cls.episode(client, item, **kwargs)
        episode.show = season.show
        episode.season = season

        # Store episode in `season`
        if season.episodes is None:
            season.episodes = {}

        season.episodes[episode.number] = episode

    @classmethod
    def episodes(cls, client, items, **kwargs):
        if not items:
            return None

        return [cls.episode(client, item, **kwargs) for item in items]

    @classmethod
    def episode(cls, client, item, **kwargs):
        if not item:
            return None

        episode = cls.construct(client, 'episode', item, **kwargs)

        if 'show' in item:
            episode.show = cls.show(client, item['show'])

        return episode
