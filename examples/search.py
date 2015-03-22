import logging
import os

logging.basicConfig(level=logging.DEBUG)

from trakt import Trakt

if __name__ == '__main__':
    # Configure
    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID')
    )

    # Lookup by id
    l_movie = Trakt['search'].lookup('tt0848228', 'imdb')
    l_show = Trakt['search'].lookup('tt0903747', 'imdb')
    l_episode = Trakt['search'].lookup('tt0959621', 'imdb')

    # Search by name
    s_movie = Trakt['search'].query('The Avengers', 'movie')
    s_show = Trakt['search'].query('Breaking Bad', 'show')

    pass
