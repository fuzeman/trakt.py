from trakt.interfaces.base import Interface, authenticated


class ShowInterface(Interface):
    path = 'show'

    def scrobble(self):
        pass
