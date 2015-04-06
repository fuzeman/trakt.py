from trakt.helpers import build_url
from trakt.interfaces.base import Interface


class OAuthInterface(Interface):
    path = 'oauth'

    def authorize_url(self, redirect_uri, response_type='code', state=None, username=None):
        client_id = self.client.configuration['client.id']

        if not client_id:
            raise ValueError('"client.id" configuration parameter is required to generate the OAuth authorization url')

        return build_url(
            self.client.base_url,
            self.path, 'authorize',

            client_id=client_id,

            redirect_uri=redirect_uri,
            response_type=response_type,
            state=state,
            username=username
        )

    def pin_url(self):
        app_id = self.client.configuration['app.id']

        if not app_id:
            raise ValueError('"app.id" configuration parameter is required to generate the PIN authentication url')

        return build_url(
            self.client.site_url,
            'pin', app_id
        )

    def token(self, code=None, redirect_uri=None, grant_type='authorization_code'):
        client_id = self.client.configuration['client.id']
        client_secret = self.client.configuration['client.secret']

        if not client_id or not client_secret:
            raise ValueError('"client.id" and "client.secret" configuration parameters are required for token exchange')

        response = self.http.post('token', data={
            'client_id': client_id,
            'client_secret': client_secret,

            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': grant_type
        })

        data = self.get_data(response)

        if not data:
            return None

        return data
