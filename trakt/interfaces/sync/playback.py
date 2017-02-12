from trakt.interfaces.base import authenticated
from trakt.interfaces.sync.core.mixins import Get, Delete


class SyncPlaybackInterface(Get, Delete):
    path = 'sync/playback'

    @authenticated
    def shows(self, store=None, **kwargs):
        raise NotImplementedError()

    @authenticated
    def episodes(self, store=None, **kwargs):
        return self.get(
            'episodes',
            store,
            **kwargs
        )

    @authenticated
    def delete_progress(self, playbackid, **kwargs):
        return self.delete(
            playbackid,
            **kwargs
        )
