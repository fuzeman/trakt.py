from helpers import authenticate

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

    for liked_list in Trakt['users'].likes('lists'):
        print liked_list

        for item in liked_list.items():
            print '\t', item
