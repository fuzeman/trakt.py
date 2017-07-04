from byte.model import Model, Property
from datetime import date, datetime


class CalendarItem(Model):
    first_aired = Property(datetime)
    released = Property(date)
