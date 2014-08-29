from trakt.interfaces.base import Interface, authenticated


class SyncBaseInterface(Interface):
    flags = {}

    @authenticated
    def get(self, media, store=None, parameters=None, access_token=None):
        path = [media]

        if parameters:
            path.extend(parameters)

        response = self.request(
            params=path,
            access_token=access_token
        )

        items = self.get_data(response)

        if type(items) is not list:
            return None

        return self.media_mapper(
            store, media, items,
            **self.flags
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
