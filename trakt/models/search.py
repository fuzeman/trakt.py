from byte.model import Model, Property


class SearchItem(Model):
    score = Property(float, nullable=True)
    type = Property(str)
