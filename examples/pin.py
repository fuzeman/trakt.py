import logging
import os

logging.basicConfig(level=logging.DEBUG)

from trakt import Trakt

if __name__ == '__main__':
    # Configure
    Trakt.base_url = 'http://api.staging.trakt.tv'

    Trakt.configuration.defaults.app(
        id=os.environ.get('APP_ID')
    )

    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID'),
        secret=os.environ.get('CLIENT_SECRET')
    )

    # Request authentication
    print 'Navigate to %s' % Trakt['oauth'].pin_url()
    pin = raw_input('Pin: ')

    # Exchange `code` for `access_token`
    details = Trakt['oauth'].token_exchange(pin, 'urn:ietf:wg:oauth:2.0:oob')

    if not details:
        print 'Token exchange failed'
        exit(1)

    access_token = details.get('access_token')
    refresh_token = details.get('refresh_token')

    # Test authentication
    print 'Using access_token: %r' % access_token

    with Trakt.configuration.oauth(access_token):
        print Trakt['sync/collection'].movies()

    # Refresh authentication with `refresh_token`
    raw_input('[token_refresh]')

    details = Trakt['oauth'].token_refresh(refresh_token, 'urn:ietf:wg:oauth:2.0:oob')
