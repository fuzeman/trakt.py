from trakt import Trakt

import logging
import os

logging.basicConfig(level=logging.DEBUG)


def authenticate():
    access_token = os.environ.get('ACCESS_TOKEN')

    if access_token:
        return access_token

    print Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob')

    code = raw_input('Authorization code:')
    if not code:
        exit(1)

    result = Trakt['oauth'].token(code, 'urn:ietf:wg:oauth:2.0:oob')
    if not result:
        exit(1)

    access_token = result.get('access_token')

    if not access_token:
        exit(1)

    print 'Access token: "%s"' % access_token
    return access_token




if __name__ == '__main__':
    # Configure
    Trakt.base_url = 'http://api.v2.trakt.tv'
    Trakt.configure(
        client_id=os.environ.get('CLIENT_ID'),
        client_secret=os.environ.get('CLIENT_SECRET')
    )

    # Authenticate
    Trakt.access_token = authenticate()

    # Fetch movie library (watched, collection, ratings)
    movies = {}

    Trakt['sync/watched'].movies(movies)
    Trakt['sync/collection'].movies(movies)

    Trakt['sync/ratings'].movies(movies)

    for key, movie in movies.items():
        print movie

        print '\t', 'keys', '\t' * 3, movie.keys
        print '\t', 'rating', '\t' * 3, movie.rating

        print '\t', 'is_watched', '\t' * 2, movie.is_watched
        print '\t', 'is_collected', '\t', movie.is_collected
        print '\t', 'collected_at', '\t', movie.collected_at
        print '\t', 'plays', '\t' * 3, movie.plays

        print
