from trakt.core.context_stack import ContextStack
from trakt.core.request import TraktRequest

from requests.adapters import HTTPAdapter
import logging
import requests
import socket
import time

log = logging.getLogger(__name__)


class HttpClient(object):
    def __init__(self, client, adapter_kwargs=None):
        self.client = client
        self.adapter_kwargs = adapter_kwargs or {}

        # Build client
        self.configuration = ContextStack()
        self.session = None

        self._build_session()

    def configure(self, path=None):
        self.configuration.push(base_path=path)

        return self

    def request(self, method, path=None, params=None, data=None, **kwargs):
        # retrieve configuration
        ctx = self.configuration.pop()

        retry = self.client.configuration.get('http.retry', True)
        max_retries = self.client.configuration.get('http.max_retries', 5)

        # build request
        if ctx.base_path and path:
            path = ctx.base_path + '/' + path
        elif ctx.base_path:
            path = ctx.base_path

        request = TraktRequest(
            self.client,
            method=method,
            path=path,
            params=params,
            data=data,

            **kwargs
        )

        prepared = request.prepare()

        # retrying requests on errors >= 500
        response = None

        for i in range(max_retries + 1):
            if i > 0 :
                log.warn('Retry # %s', i)

            try:
                response = self.session.send(prepared)
            except socket.gaierror, e:
                code, _ = e

                if code != 8:
                    raise e

                log.warn('Encountered socket.gaierror (code: 8)')

                response = self._build_session().send(prepared)
            except requests.exceptions.ConnectionError,e:
                log.warn("Encountered Connection errors , will retry")    

            if not retry or not response or response.status_code < 500:
                break

            if response is not None and response.status_code is not None:         
                log.warn('Continue retry since status is %s', response.status_code)
            time.sleep(5)

        return response

    def get(self, path=None, params=None, data=None, **kwargs):
        return self.request('GET', path, params, data, **kwargs)

    def post(self, path=None, params=None, data=None, **kwargs):
        return self.request('POST', path, params, data, **kwargs)

    def delete(self, path=None, params=None, data=None, **kwargs):
        return self.request('DELETE', path, params, data, **kwargs)

    def _build_session(self):
        if self.session:
            log.info('Rebuilding session and connection pools...')

        # Build the connection pool
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(**self.adapter_kwargs))
        self.session.mount('https://', HTTPAdapter(**self.adapter_kwargs))

        return self.session
