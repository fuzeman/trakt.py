from helpers import authenticate

from trakt import Trakt
import logging
import os

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    # Configure
    Trakt.base_url = 'http://api.v2.trakt.tv'

    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID'),
        secret=os.environ.get('CLIENT_SECRET')
    )

    Trakt.configuration.defaults.oauth(
        token=authenticate()
    )

    # Fetch movie library (watched, collection, ratings)
    movies = {}

    # Trakt['sync/watched'].movies(movies)
    # Trakt['sync/collection'].movies(movies)
    #
    # Trakt['sync/ratings'].movies(movies)

    for key, movie in movies.items():
        print movie

        print '\t', 'keys', '\t' * 3, movie.keys
        print '\t', 'rating', '\t' * 3, movie.rating

        print '\t', 'is_watched', '\t' * 2, movie.is_watched
        print '\t', 'is_collected', '\t', movie.is_collected
        print '\t', 'collected_at', '\t', movie.collected_at
        print '\t', 'plays', '\t' * 3, movie.plays

        print

    # Fetch show/episode library (watched, collection, ratings)
    shows = {}

    Trakt['sync/watched'].shows(shows)
    Trakt['sync/collection'].shows(shows)

    Trakt['sync/ratings'].shows(shows)
    Trakt['sync/ratings'].episodes(shows)

    for key, show in shows.items():
        print show

        print '\t', 'keys', '\t' * 3, show.keys
        print '\t', 'rating', '\t' * 3, show.rating
        print

        for season_num, season in show.seasons.items():

            print '\t', season

            for episode_num, episode in season.episodes.items():
                print '\t' * 2, episode

                print '\t' * 3, 'rating', '\t' * 3, episode.rating

                print '\t' * 3, 'is_watched', '\t' * 2, episode.is_watched
                print '\t' * 3, 'is_collected', '\t', episode.is_collected
                print '\t' * 3, 'collected_at', '\t', episode.collected_at
                print '\t' * 3, 'plays', '\t' * 3, episode.plays
                print

        print
