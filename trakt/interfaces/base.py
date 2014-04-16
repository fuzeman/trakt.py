from trakt.helpers import parse_credentials

from functools import wraps


class Interface(object):
    def __init__(self, client):
        self.client = client


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
