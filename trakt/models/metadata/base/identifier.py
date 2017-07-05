from byte.model import Model, Property


class Identifier(Model):
    name = Property(str, name='key')
    value = Property((int, str))

    def to_tuple(self):
        if not self.name or not self.value:
            return None

        return self.name, self.value
