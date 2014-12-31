from trakt import Trakt

import os


def authenticate():
    access_token = os.environ.get('ACCESS_TOKEN')

    if access_token:
        return access_token

    print Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob')

    code = raw_input('Authorization code:')
    if not code:
        exit(1)

    result = Trakt['oauth'].token(code, 'urn:ietf:wg:oauth:2.0:oob')
    if not result:
        exit(1)

    access_token = result.get('access_token')

    if not access_token:
        exit(1)

    print 'Access token: "%s"' % access_token
    return access_token
