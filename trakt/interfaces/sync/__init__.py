from trakt.interfaces.base import Interface


class SyncInterface(Interface):
    path = 'sync'

    def last_activities(self):
        return self.request('lastactivities')

    def playback(self):
        return self.request('playback')
