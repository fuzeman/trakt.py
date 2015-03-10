import logging
import os

logging.basicConfig(level=logging.DEBUG)

from trakt import Trakt

if __name__ == '__main__':
    # Configure
    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID')
    )

    # Login
    username = os.environ.get('USERNAME')
    token = os.environ.get('AUTH_TOKEN')

    if token is None:
        # Attempt authentication (retrieve new token)
        token = Trakt['auth'].login(username, os.environ.get('PASSWORD'))

    print 'Using token: %r' % token

    with Trakt.configuration.auth(username, token):
        print Trakt['sync/collection'].movies()

    with Trakt.configuration.auth(username, token):
            with Trakt.configuration.http(retry=True):
                print Trakt['movies'].get('tron-legacy-2010') #use only traktId, trakt slug or imdbId

    with Trakt.configuration.auth(username, token):
            with Trakt.configuration.http(retry=True):
                print Trakt['shows'].get(1390) #use only traktId, trakt slug or imdbId

    with Trakt.configuration.auth(username, token):
            with Trakt.configuration.http(retry=True):
                print Trakt['shows'].seasons('tt0944947')

    with Trakt.configuration.auth(username, token):
            with Trakt.configuration.http(retry=True):
                print Trakt['shows'].season('game-of-thrones', 1)

    with Trakt.configuration.auth(username, token):
            with Trakt.configuration.http(retry=True):
                print Trakt['shows'].episode('game-of-thrones', 1, 1)