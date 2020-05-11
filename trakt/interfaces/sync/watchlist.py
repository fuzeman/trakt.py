from __future__ import absolute_import, division, print_function

from trakt.interfaces.base import authenticated
from trakt.interfaces.sync.core.mixins import Get, Add, Remove


class SyncWatchlistInterface(Get, Add, Remove):
    path = 'sync/watchlist'
    flags = {'in_watchlist': True}

    def get(self, media=None, start_at=None, end_at=None, store=None, extended=None, flat=False, page=None,
            per_page=None, **kwargs):

        if media and not flat and page is not None:
            raise ValueError('`page` parameter is only supported with `flat=True`')

        # Build query
        query = {
            'extended': extended,
            'page': page,
            'limit': per_page
        }

        # Request watched history
        return super(SyncWatchlistInterface, self).get(
            media, store,
            query=query,
            flat=flat or media is None,
            **kwargs
        )

    @authenticated
    def seasons(self, store=None, **kwargs):
        return self.get(
            'seasons',
            store=store,
            **kwargs
        )

    @authenticated
    def episodes(self, store=None, **kwargs):
        return self.get(
            'episodes',
            store=store,
            **kwargs
        )
