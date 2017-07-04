from byte.model import Model, Property


class Airs(Model):
    day = Property(str)
    time = Property(str)

    timezone = Property(str)
