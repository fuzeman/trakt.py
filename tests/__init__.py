from __future__ import absolute_import, division, print_function

from trakt import Trakt

import logging


# Enable DEBUG Logging
logging.basicConfig(level=logging.DEBUG)

# Setup client defaults
Trakt.configuration.defaults.client(
    id='mock-client_id',
    secret='mock-client_secret'
)
