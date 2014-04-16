from .base import Interface, authenticated


class AccountInterface(Interface):
    @authenticated
    def test(self, credentials=None):
        response = self.client.request('account/test', credentials=credentials)

        # unknown result - no response or server error
        if response is None or response.status_code >= 500:
            return None

        data = response.json()

        # unknown result - no json data returned
        if not data:
            return None

        return data.get('status') == 'success'
