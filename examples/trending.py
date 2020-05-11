from __future__ import absolute_import, division, print_function

from trakt import Trakt

import logging
import os

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    # Configure
    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID')
    )

    # Print trending movies
    items = Trakt['movies'].trending(pagination=True, per_page=25)

    print('Found %d trending movie(s) [%d page(s)]' % (items.total_items, items.total_pages))

    for item in items.get(1):  # Retrieve first page
        print('\t%s (%s)' % (item.title, item.year))

    # Print trending shows
    items = Trakt['shows'].trending(pagination=True, per_page=25)

    print('Found %d trending shows(s) [%d page(s)]' % (items.total_items, items.total_pages))

    for item in items.get(1):  # Retrieve first page
        print('\t%s (%s)' % (item.title, item.year))
