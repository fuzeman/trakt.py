from trakt.helpers import parse_credentials

from functools import wraps


class Interface(object):
    path = None

    def __init__(self, client):
        self.client = client


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
