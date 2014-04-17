from trakt.interfaces.base import Interface, authenticated


class UserLibraryInterface(Interface):
    path = 'user/library'

    @authenticated
    def get(self, media, library, username=None, extended=None, store=None, credentials=None):
        # Fill username with currently authenticated user (if nothing is provided)
        if username is None:
            username = credentials.get('username')

        response = self.request(
            '%s/%s.json' % (media, library),
            [username, extended],
            credentials=credentials
        )

        items = self.get_data(response)
        flags = self.get_flags(library)

        return self.media_mapper(store, media, items, **flags)

    @staticmethod
    def get_flags(library):
        if library == 'collection':
            return {'is_collected': True}

        if library == 'watched':
            return {'is_watched': True}

        return {}

    @authenticated
    def all(self, media, username=None, extended=None, store=None, credentials=None):
        return self.get(
            media, 'all',
            username, extended,
            store=store,
            credentials=credentials
        )

    @authenticated
    def collection(self, media, username=None, extended=None, store=None, credentials=None):
        return self.get(
            media, 'collection',
            username, extended,
            store=store,
            credentials=credentials
        )

    @authenticated
    def watched(self, media, username=None, extended=None, store=None, credentials=None):
        return self.get(
            media, 'watched',
            username, extended,
            store=store,
            credentials=credentials
        )
