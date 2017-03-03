from __future__ import absolute_import, division, print_function

from trakt import Trakt

import json
import os
import six


def authenticate():
    authorization = os.environ.get('AUTHORIZATION')

    if authorization:
        return json.loads(authorization)

    print('Navigate to: %s' % Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob'))

    code = six.moves.input('Authorization code:')
    if not code:
        exit(1)

    authorization = Trakt['oauth'].token(code, 'urn:ietf:wg:oauth:2.0:oob')
    if not authorization:
        exit(1)

    print('Authorization: %r' % authorization)
    return authorization
