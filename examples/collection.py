from trakt import Trakt

import logging
import os

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    Trakt.configure(
        api_key=os.environ.get('API_KEY'),
        credentials=('test', 'test')
    )

    store = {}

    # Fetch library
    Trakt['user/library/shows'].watched('fuzeman-dev', store=store)
    Trakt['user/library/shows'].collection('fuzeman-dev', store=store)

    # Fetch ratings
    Trakt['user/ratings'].episodes('fuzeman-dev', store=store)

    for key, show in store.items():
        print show

        print '\t', 'keys', '\t' * 3, show.keys
        print '\t', 'rating', '\t' * 3, show.rating

        print
        for key, episode in show.episodes.items():
            print '\t', episode

            print '\t' * 2, 'keys', '\t' * 3, episode.keys
            print '\t' * 2, 'rating', '\t' * 3, episode.rating
            print '\t' * 2, 'is_watched', '\t' * 2, episode.is_watched
            print '\t' * 2, 'is_collected', '\t', episode.is_collected
            print

        print
