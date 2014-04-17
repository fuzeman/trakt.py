from trakt.interfaces.base import Interface, authenticated


class UserRatingsInterface(Interface):
    path = 'user/ratings'

    @authenticated
    def get(self, media, username=None, rating='all', extended=None, store=None, credentials=None):
        # Fill username with currently authenticated user (if nothing is provided)
        if username is None:
            username = credentials.get('username')

        response = self.request(
            '%s.json' % media,
            [username, rating, extended],
            credentials=credentials
        )

        items = self.get_data(response)

        return self.media_mapper(store, media, items)

    @authenticated
    def episodes(self, username=None, rating='all', extended=None, store=None, credentials=None):
        return self.get(
            'episodes', username,
            rating, extended,
            store=store,
            credentials=credentials
        )

    @authenticated
    def movies(self, username=None, rating='all', extended=None, store=None, credentials=None):
        return self.get(
            'movies', username,
            rating, extended,
            credentials=credentials
        )

    @authenticated
    def shows(self, username=None, rating='all', extended=None, store=None, credentials=None):
        return self.get(
            'shows', username,
            rating, extended,
            store=store,
            credentials=credentials
        )
