from trakt.helpers import parse_credentials

from functools import wraps


class Interface(object):
    path = None

    def __init__(self, client):
        self.client = client

    def request(self, path, params=None, data=None, credentials=None, **kwargs):
        path = '%s/%s' % (self.path, path)

        return self.client.request(path, params, data, credentials, **kwargs)

    @staticmethod
    def get_data(response):
        # unknown result - no response or server error
        if response is None or response.status_code >= 500:
            return None

        data = response.json()

        # unknown result - no json data returned
        if not data:
            return None

        return data


class InterfaceProxy(object):
    def __init__(self, interface, args):
        self.interface = interface
        self.args = list(args)

    def __getattr__(self, name):
        value = getattr(self.interface, name)

        if not hasattr(value, '__call__'):
            return value

        @wraps(value)
        def wrap(*args, **kwargs):
            args = self.args + list(args)

            return value(*args, **kwargs)

        return wrap


def authenticated(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if args and isinstance(args[0], Interface):
            interface = args[0]

            if 'credentials' not in kwargs:
                kwargs['credentials'] = interface.client.credentials
            else:
                kwargs['credentials'] = parse_credentials(kwargs['credentials'])

        return func(*args, **kwargs)

    return wrap
