from __future__ import absolute_import, division, print_function

from trakt.interfaces.base import authenticated
from trakt.interfaces.sync.core.mixins import Get, Add, Remove


class SyncRatingsInterface(Get, Add, Remove):
    path = 'sync/ratings'

    @authenticated
    def get(self, media=None, store=None, rating=None, extended=None, flat=False, page=None, per_page=None, **kwargs):
        if media and not flat and page is not None:
            raise ValueError('`page` parameter is only supported with `flat=True`')

        # Build parameters
        params = []

        if rating is not None:
            params.append(rating)

        # Build query
        query = {
            'extended': extended,
            'page': page,
            'limit': per_page
        }

        # Request ratings
        return super(SyncRatingsInterface, self).get(
            media, store, params,
            flat=flat or media is None,
            query=query,
            **kwargs
        )

    #
    # Shortcut methods
    #

    @authenticated
    def shows(self, store=None, rating=None, **kwargs):
        return self.get('shows', store, rating, **kwargs)

    @authenticated
    def seasons(self, store=None, rating=None, **kwargs):
        return self.get('seasons', store, rating, **kwargs)

    @authenticated
    def episodes(self, store=None, rating=None, **kwargs):
        return self.get('episodes', store, rating, **kwargs)

    @authenticated
    def movies(self, store=None, rating=None, **kwargs):
        return self.get('movies', store, rating, **kwargs)
