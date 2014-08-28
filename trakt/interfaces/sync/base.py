from trakt.interfaces.base import Interface, authenticated


class SyncBaseInterface(Interface):
    @authenticated
    def get(self, media, store=None, access_token=None):
        response = self.request(
            media,
            access_token=access_token
        )

        items = self.get_data(response)

        if type(items) is not list:
            return None

        return self.media_mapper(
            store, media, items,
            is_collected=True
        )

    @authenticated
    def post(self, data, access_token=None):
        response = self.request(
            method='POST',
            data=data,
            access_token=access_token
        )

        data = self.get_data(response)

        if not data:
            return False

        return data

    @authenticated
    def delete(self, data, access_token=None):
        pass

    #
    # Shortcut methods
    #

    @authenticated
    def shows(self, store=None, access_token=None):
        return self.get(
            'shows',
            store=store,
            access_token=access_token
        )

    @authenticated
    def movies(self, store=None, access_token=None):
        return self.get(
            'movies',
            store=store,
            access_token=access_token
        )
