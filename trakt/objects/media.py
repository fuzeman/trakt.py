from trakt.objects.core.helpers import update_attributes
from trakt.objects.rating import Rating


class Media(object):
    def __init__(self, client, keys=None):
        self._client = client

        self.keys = keys

        self.images = None
        self.overview = None
        self.rating = None
        self.score = None

        # Flags
        self.in_watchlist = None

    @property
    def pk(self):
        if not self.keys:
            return None

        return self.keys[0]

    def _update(self, info=None, in_watchlist=None, **kwargs):
        update_attributes(self, info, [
            'overview',
            'images',
            'score'
        ])

        self.rating = Rating._construct(self._client, info) or self.rating

        # Set flags
        if in_watchlist is not None:
            self.in_watchlist = in_watchlist

    def __str__(self):
        return self.__repr__()
