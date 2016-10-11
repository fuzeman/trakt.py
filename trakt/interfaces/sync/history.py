from trakt.interfaces.sync.core.mixins import Get, Add, Remove


class SyncHistoryInterface(Get, Add, Remove):
    path = 'sync/history'

    def get(self, media=None, store=None, params=None, page=1, per_page=10, **kwargs):
        # Build query
        query = {}

        if page:
            query['page'] = page

        if per_page:
            query['limit'] = per_page

        # Request watched history
        return super(SyncHistoryInterface, self).get(
            media=media,
            store=store,
            params=params,

            query=query,
            flat=True,
            **kwargs
        )
