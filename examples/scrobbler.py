from helpers import authenticate

from pprint import pprint
from trakt import Trakt
import logging
import os
import time

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    # Configure
    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID'),
        secret=os.environ.get('CLIENT_SECRET')
    )

    # Authenticate
    Trakt.configuration.defaults.oauth.from_response(
        authenticate()
    )

    # movie = {
    #     'title': 'Guardians of the Galaxy',
    #     'year': 2014,
    #     'ids': {
    #         'trakt': 28,
    #         'slug': 'guardians-of-the-galaxy-2014',
    #         'imdb': 'tt2015381',
    #         'tmdb': 118340
    #     }
    # }

    show = {
        "title": "Breaking Bad",
        "year": 2008,
        "ids": {
            "trakt": 1,
            "slug": "breaking-bad",
            "tvdb": 81189,
            "imdb": "tt0903747",
            "tmdb": 1396,
            "tvrage": 18164
        }
    }

    episode = {
        "season": 1,
        "number": 1,
        "title": "Pilot",
        "ids": {
            "trakt": 16,
            "tvdb": 349232,
            "imdb": "tt0959621",
            "tmdb": 62085,
            "tvrage": 637041
        }
    }

    # - Start watching
    pprint(Trakt['scrobble'].start(
        show=show,
        episode=episode,
        progress=45
    ))

    time.sleep(10)

    pprint(Trakt['scrobble'].stop(
        show=show,
        episode=episode,
        progress=90
    ))
