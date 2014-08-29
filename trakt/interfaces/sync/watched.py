from trakt.interfaces.sync.base import SyncBaseInterface


class SyncWatchedInterface(SyncBaseInterface):
    path = 'sync/watched'
    flags = {'is_watched': True}
