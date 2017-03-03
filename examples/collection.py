from __future__ import absolute_import, division, print_function

from examples.helpers import authenticate
from trakt import Trakt
from trakt.objects import Movie, Show

import logging
import os

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    # Configure
    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID'),
        secret=os.environ.get('CLIENT_SECRET')
    )

    Trakt.configuration.defaults.http(
        retry=True
    )

    # Authenticate
    Trakt.configuration.defaults.oauth.from_response(
        authenticate()
    )

    # Fetch playback for movies
    playback = Trakt['sync/playback'].movies(exceptions=True)

    for item in playback.values():
        print(item)

        if type(item) is Movie:
            print('\tprogress: %r' % item.progress)
            print('\tpaused_at: %r' % item.paused_at)

    # Fetch movie library (watched, collection, ratings)
    movies = {}

    Trakt['sync/watched'].movies(movies, exceptions=True)
    Trakt['sync/collection'].movies(movies, exceptions=True)

    Trakt['sync/ratings'].movies(movies, exceptions=True)

    for movie in movies.values():
        print(movie)

        print('\tkeys%s%r' % ('\t' * 3, movie.keys))
        print('\trating%s%r' % ('\t' * 3, movie.rating))

        print('\tis_watched%s%r' % ('\t' * 2, movie.is_watched))
        print('\tlast_watched_at%s%r' % ('\t', movie.last_watched_at))
        print('\tis_collected%s%r' % ('\t', movie.is_collected))
        print('\tcollected_at%s%r' % ('\t', movie.collected_at))
        print('\tplays%s%r' % ('\t' * 3, movie.plays))

        print('')

    # Fetch playback for shows
    playback = Trakt['sync/playback'].episodes(exceptions=True)

    for item in playback.values():
        print(item)

        if type(item) is Show:
            for _, episode in item.episodes():
                print('\t%r' % (episode,))

                print('\t\tprogress: %r' % episode.progress)
                print('\t\tpaused_at: %r' % episode.paused_at)

    # Fetch show/episode library (watched, collection, ratings)
    shows = {}

    Trakt['sync/watched'].shows(shows, exceptions=True)
    Trakt['sync/collection'].shows(shows, exceptions=True)

    Trakt['sync/ratings'].shows(shows, exceptions=True)
    Trakt['sync/ratings'].episodes(shows, exceptions=True)

    for show in shows.values():
        print(show)

        print('\tkeys%s%r' % ('\t' * 3, show.keys))
        print('\trating%s%r' % ('\t' * 3, show.rating))
        print('')
