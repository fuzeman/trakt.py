from __future__ import absolute_import, division, print_function

from examples.helpers import authenticate

import logging
import os


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    from trakt import Trakt

    # Configure
    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID'),
        secret=os.environ.get('CLIENT_SECRET')
    )

    # Authenticate
    Trakt.configuration.defaults.oauth.from_response(
        authenticate()
    )

    # Retrieve lists
    lists = Trakt['users'].likes('lists', pagination=True)

    print('Found %d list(s) [%d page(s)]' % (
        lists.total_items,
        lists.total_pages
    ))

    for x, liked_list in enumerate(lists):
        items = liked_list.items(pagination=True, per_page=10)

        print('[%d/%d] %r [%d item(s), %d page(s)]' % (
            x + 1,
            lists.total_items,
            liked_list,
            items.total_items,
            items.total_pages
        ))

        for y, item in enumerate(items):
            print('\t[%s/%s] %r' % (
                y + 1,
                items.total_items,
                item
            ))

            # Only print 20 items in the list
            if y + 1 >= 20:
                break
