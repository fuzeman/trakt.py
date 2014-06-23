from trakt import Trakt

from pprint import pprint
import hashlib
import logging
import os
import time

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    password = hashlib.sha1(os.environ.get('PASSWORD'))

    Trakt.configure(
        api_key=os.environ.get('API_KEY'),
        credentials=(
            os.environ.get('USERNAME'),
            password.hexdigest()
        )
    )

    pprint(Trakt['show'].watching(
        title='Community',
        year=2009,

        season=5,
        episode=13,

        duration=26,
        progress=45
    ))

    time.sleep(10)

    Trakt['show'].cancelwatching()
