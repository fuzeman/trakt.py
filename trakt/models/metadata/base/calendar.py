from byte.model import Model, Property
from datetime import date, datetime


class Calendar(Model):
    first_aired = Property(datetime)
    released = Property(date)
