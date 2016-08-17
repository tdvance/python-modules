class Tag:
    def __init__(self, name, value=None):
        self._name = str(name)
        self._value = set([value]).pop()  # trick to ensure hashability
        self._key = Tag.normalize(self._name)

    @classmethod
    def normalize(cls, name):
        x = str(name).strip().lower()
        x = '_'.join(x.split())
        x = x.split('_')
        x = [y for y in x if y]
        x = '_'.join(x)
        return x

    @property
    def name(self):
        return self._name

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    def __str__(self):
        if self._value is not None:
            return self.name + '=' + str(self.value)
        return self.name

    def __repr__(self):
        return 'Tag(name=%r, value=%r)' % (self.name, self.value)

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

    def has_value(self):
        return self.value is not None
