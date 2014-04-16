from trakt.interfaces.base import Interface


class UserLibraryInterface(Interface):
    path = 'user/library'

    def all(self, media):
        return 'user/library/%s/all' % media

    def collection(self, media):
        return 'user/library/%s/collection' % media

    def watched(self, media):
        return 'user/library/%s/watched' % media
