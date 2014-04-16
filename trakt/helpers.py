def build_repr(obj, keys):
    key_part = ', '.join([
        ('%s: %s' % (key, repr(getattr(obj, key))))
        for key in keys
    ])

    cls = getattr(obj, '__class__')

    return '<%s %s>' % (getattr(cls, '__name__'), key_part)


def setdefault(d, defaults):
    for key, value in defaults.items():
        d.setdefault(key, value)


def parse_credentials(value):
    if type(value) is dict:
        return value

    if hasattr(value, '__iter__') and len(value) == 2:
        return {
            'username': value[0],
            'password': value[1]
        }

    return value


def has_attribute(obj, name):
    try:
        object.__getattribute__(obj, name)
        return True
    except AttributeError:
        return False
