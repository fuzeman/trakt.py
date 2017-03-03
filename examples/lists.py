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

    for x, liked_list in enumerate(Trakt['users'].likes('lists', pagination=True)):
        print('[%s] %r' % (x + 1, liked_list))

        items = liked_list.items()

        if not items:
            print(' - ERROR')
            continue

        items = list(items)
        print(' - %d item(s)' % len(items))
