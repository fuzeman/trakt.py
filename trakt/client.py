from trakt.core.context import Context
from trakt.interfaces import construct_map
from trakt.interfaces.base import InterfaceProxy
from trakt.request import TraktRequest

import logging
import requests
import socket

log = logging.getLogger(__name__)


class TraktClient(object):
    base_url = 'http://api.trakt.tv'
    interfaces = None

    def __init__(self):
        self.client_id = None
        self.client_secret = None

        self.access_token = None

        # Scrobbling parameters
        self.app_version = None
        self.app_date = None

        # Private
        self._session = requests.Session()
        self._context_stack = [Context(self)]

        # Construct interfaces
        self.interfaces = construct_map(self)

    @property
    def current(self):
        if not self._context_stack:
            return None

        return self._context_stack[-1]

    def context(self, access_token=None):
        return Context(self, access_token)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise ValueError('Unknown option "%s" specified' % key)

            setattr(self, key, value)

    def request(self, path, params=None, data=None, **kwargs):
        request = TraktRequest(
            self,
            path=path,
            params=params,
            data=data,

            **kwargs
        )

        prepared = request.prepare()

        # TODO retrying requests on 502, 503 errors?

        try:
            return self._session.send(prepared)
        except socket.gaierror, e:
            code, _ = e

            if code != 8:
                raise e

            log.warn('Encountered socket.gaierror (code: 8)')

            return self._rebuild().send(prepared)

    def _rebuild(self):
        log.info('Rebuilding session and connection pools...')

        # Rebuild the connection pool (old pool has stale connections)
        self._session = requests.Session()

        return self._session

    def __getitem__(self, path):
        parts = path.strip('/').split('/')

        cur = self.interfaces

        while parts and type(cur) is dict:
            key = parts.pop(0)

            if key not in cur:
                return None

            cur = cur[key]

        if type(cur) is dict:
            cur = cur.get(None)

        if parts:
            return InterfaceProxy(cur, parts)

        return cur
