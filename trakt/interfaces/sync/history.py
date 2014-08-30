from trakt.interfaces.sync.base import SyncBaseInterface


class SyncHistoryInterface(SyncBaseInterface):
    path = 'sync/history'

    def get(self, media, store=None, parameters=None):
        raise Exception("Invalid request")
