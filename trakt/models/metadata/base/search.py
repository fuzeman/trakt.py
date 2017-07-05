from byte.model import Model, Property


class Search(Model):
    score = Property(float, nullable=True)
    type = Property(str)
