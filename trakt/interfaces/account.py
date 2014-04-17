from trakt.interfaces.base import Interface, authenticated


class AccountInterface(Interface):
    path = 'account'

    @authenticated
    def test(self, credentials=None):
        response = self.request('test', credentials=credentials)
        data = self.get_data(response)

        if data is None:
            return None

        return data.get('status') == 'success'
