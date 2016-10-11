from helpers import authenticate

from trakt import Trakt
import os
import six


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

    # Retrieve 10 history records (most recent)
    print('Latest records:')

    for x, item in enumerate(Trakt['sync/history'].get(per_page=10)):
        print(' - [%02d] %-120s (watched_at: %r)' % (x, repr(item), item.watched_at.strftime('%Y-%m-%d %H:%M:%S')))

    print('')
    print('=' * 150)
    print('')

    # Retrieve all history records
    print('Entire history:')

    for x, item in enumerate(Trakt['sync/history'].get(pagination=True, per_page=25)):
        print(' - [%02d] %-120s (watched_at: %r)' % (x, repr(item), item.watched_at.strftime('%Y-%m-%d %H:%M:%S')))

        # Prompt every 25 items
        if x != 0 and not (x % 24) and six.moves.input('Load next page? [yes]: ') not in ['', 'y', 'yes']:
            break
