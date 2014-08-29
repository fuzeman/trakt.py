from trakt.interfaces.oauth import OAuthInterface
from trakt.interfaces.scrobble import ScrobbleInterface
from trakt.interfaces.sync import SyncInterface
from trakt.interfaces.sync.collection import SyncCollectionInterface
from trakt.interfaces.sync.history import SyncHistoryInterface
from trakt.interfaces.sync.ratings import SyncRatingsInterface
from trakt.interfaces.sync.watched import SyncWatchedInterface


# TODO automatic interface discovery
INTERFACES = [
    # /
    OAuthInterface,
    ScrobbleInterface,

    # /sync
    SyncInterface,
    SyncCollectionInterface,
    SyncHistoryInterface,
    SyncRatingsInterface,
    SyncWatchedInterface
]


def get_interfaces():
    for interface in INTERFACES:
        if not interface.path:
            continue

        path = interface.path.strip('/')

        if path:
            path = path.split('/')
        else:
            path = []

        yield path, interface


def construct_map(client, d=None, interfaces=None):
    if d is None:
        d = {}

    if interfaces is None:
        interfaces = get_interfaces()

    for path, interface in interfaces:
        if len(path) == 0:
            continue

        key = path.pop(0)

        if len(path) == 0:
            d[key] = interface(client)
            continue

        value = d.get(key, {})

        if type(value) is not dict:
            value = {None: value}

        construct_map(client, value, [(path, interface)])

        d[key] = value

    return d
