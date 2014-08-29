from trakt.interfaces.base import authenticated
from trakt.interfaces.sync.base import SyncBaseInterface


class SyncRatingsInterface(SyncBaseInterface):
    path = 'sync/ratings'

    @authenticated
    def get(self, media, store=None, rating=None, access_token=None):
        parameters = []

        if rating is not None:
            parameters.append(rating)

        super(SyncRatingsInterface, self).get(media, store, parameters, access_token=access_token)

    #
    # Shortcut methods
    #

    @authenticated
    def shows(self, store=None, rating=None, access_token=None):
        return self.get(
            'shows', store, rating,
            access_token=access_token
        )

    @authenticated
    def seasons(self, store=None, rating=None, access_token=None):
        return self.get(
            'seasons', store, rating,
            access_token=access_token
        )

    @authenticated
    def episodes(self, store=None, rating=None, access_token=None):
        return self.get(
            'episodes', store, rating,
            access_token=access_token
        )

    @authenticated
    def movies(self, store=None, rating=None, access_token=None):
        return self.get(
            'movies', store, rating,
            access_token=access_token
        )
