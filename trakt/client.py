from trakt.helpers import parse_credentials
from trakt.interfaces.account import AccountInterface
from trakt.request import TraktRequest

import requests


class TraktClient(object):
    base_url = 'http://api.trakt.tv'

    interfaces = {
        'account': AccountInterface
    }

    def __init__(self):
        self.api_key = None

        # Scrobbling parameters
        self.plugin_version = None
        self.media_center_version = None

        # Private
        self._session = requests.Session()

        self._get_credentials = None

        # Construct interfaces
        for key, value in self.interfaces.items():
            self.interfaces[key] = value(self)

    def request(self, path, params=None, data=None, credentials=None, **kwargs):
        request = TraktRequest(
            self,
            path=path,

            params=params,
            data=data,

            credentials=credentials,
            **kwargs
        )

        prepared = request.prepare()

        # TODO retrying requests on 502, 503 errors
        return self._session.send(prepared)

    def __getitem__(self, key):
        return self.interfaces.get(key)

    @property
    def credentials(self):
        return parse_credentials(self._get_credentials())

    @credentials.setter
    def credentials(self, value):
        if hasattr(value, '__iter__'):
            self._get_credentials = lambda: value
        elif hasattr(value, '__call__'):
            self._get_credentials = value
        else:
            raise ValueError('(<username>, <password>) iterable, or function is required')
