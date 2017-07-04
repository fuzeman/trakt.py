import warnings


def property_proxy(name, targets, deprecated=False, message=None):
    @property
    def prop(self):
        # Display deprecation warning (if enabled)
        if deprecated:
            warnings.warn(message or build_message(self.__class__, name, targets), DeprecationWarning, stacklevel=2)

        # Find property in `targets`
        for target in targets:
            instance = getattr(self, target)

            if not hasattr(instance, name):
                continue

            return getattr(instance, name)

        return None

    return prop


def build_message(cls, name, targets):
    return '`%s.%s` has been deprecated, use: %s' % (
        cls.__name__, name, ', '.join([
            '`%s.%s.%s`' % (cls.__name__, target, name)
            for target in targets
        ])
    )
