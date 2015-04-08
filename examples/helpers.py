from trakt import Trakt

import json
import os


def authenticate():
    authorization = os.environ.get('AUTHORIZATION')

    if authorization:
        return json.loads(authorization)

    print Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob')

    code = raw_input('Authorization code:')
    if not code:
        exit(1)

    authorization = Trakt['oauth'].token(code, 'urn:ietf:wg:oauth:2.0:oob')
    if not authorization:
        exit(1)

    print "Authorization: %r" % authorization
    return authorization
