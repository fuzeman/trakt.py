from byte.model import Model, Property


class Trending(Model):
    watchers = Property(int)
