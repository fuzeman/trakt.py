import warnings


def get_path(value, path):
    for name in path.split('.'):
        if not hasattr(value, name):
            return None

        value = getattr(value, name)

    return value


def property_proxy(target, deprecated=False, message=None):
    @property
    def prop(self):
        # Display deprecation warning (if enabled)
        if deprecated:
            warnings.warn(message or build_message(self.__class__, target), DeprecationWarning, stacklevel=2)

        # Retrieve property value
        return get_path(self, target)

    return prop


def build_message(cls, target):
    pos = target.rfind('.')

    if pos < 0:
        pos = 0
    else:
        pos += 1

    key = target[pos:]

    return '`%s.%s` has been deprecated, use: `%s.%s`' % (
        cls.__name__, key,
        cls.__name__, target
    )
