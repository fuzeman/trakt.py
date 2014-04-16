from trakt.client import TraktClient


class TraktMeta(type):
    def __getattr__(self, name):
        if self.__hasattr(self, name):
            return super(TraktMeta, self).__getattribute__(name)

        if self.client is None:
            self.construct()

        return getattr(self.client, name)

    def __setattr__(self, name, value):
        if self.__hasattr(self, name):
            return super(TraktMeta, self).__setattr__(name, value)

        if self.client is None:
            self.construct()

        setattr(self.client, name, value)

    def __getitem__(self, key):
        if self.client is None:
            self.construct()

        return self.client[key]

    def __hasattr(self, obj, name):
        try:
            object.__getattribute__(obj, name)
            return True
        except AttributeError:
            return False


class Trakt(object):
    __metaclass__ = TraktMeta

    client = None

    @classmethod
    def construct(cls):
        cls.client = TraktClient()
