import logging
import os

logging.basicConfig(level=logging.DEBUG)

from trakt import Trakt
from trakt.objects import Season, Episode


def print_lookup(id, service):
    print "Trakt['search'].lookup(%r, %r)" % (id, service)

    item = Trakt['search'].lookup(id, service)

    if type(item) is Episode and item.show:
        sk, ek = item.pk
        print "\t%s (%s) - S%02dE%02d %r" % (item.show.title, item.show.year, sk, ek, item.title)
    else:
        print "\t%s (%s)" % (item.title, item.year)


def print_query(query, media=None, year=None):
    print "Trakt['search'].query(%r, %r, %r)" % (query, media, year)

    items = Trakt['search'].query(query, media, year)

    for item in items:
        if type(item) is Episode and item.show:
            sk, ek = item.pk
            print "\t[%.2d%%] %s (%s) - S%02dE%02d %r" % (item.score, item.show.title, item.show.year, sk, ek, item.title)
        else:
            print "\t[%.2d%%] %s (%s)" % (item.score, item.title, item.year)


if __name__ == '__main__':
    # Configure
    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID')
    )

    # Lookup by id
    print_lookup('tt0848228', 'imdb')
    print_lookup('tt0903747', 'imdb')
    print_lookup('tt0959621', 'imdb')

    # Search by name
    print_query('The Avengers', 'movie')
    print_query('Breaking Bad', 'show')
    print_query('Breaking Bad', 'episode')
