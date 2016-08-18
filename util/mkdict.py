class MKDict:
    def __init__(self):
        self._data = dict()

    def __len__(self):
        return len(self._data)

    def __contains__(self, tagset):
        return tagset in self._data

    def __getitem__(self, tagset):
        return self._data[tagset]

    def __setitem__(self, tagset, value):
        self._data[tagset] = value

    def __delitem__(self, tagset):
        del self._data[tagset]

    def __eq__(self, other):
        return self._data == other._data

    def pop(self, tagset, default=KeyError):
        if default is KeyError or tagset in self:
            v = self[tagset]
            del self[tagset]
            return v
        else:
            return default

    def copy(self):
        result = MKDict()
        result._data = self._data.copy()
        return result

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def __iter__(self):
        return iter(self._data)

    def clear(self):
        self._data.clear()

    def get(self, tagset, default=None):
        return self.pop(tagset, default)

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def popitem(self):
        return self._data.popitem()

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def values(self):
        return self._data.values()

    def find(self, tagsubset, fuzz=1.0):
        """

        :param tagsubset: tagset to be (approximately) a subset of the
        returned tag sets.
        :param fuzz: should be between 0.0 (yield everything) and 1.0 (
        yield true supersets)  e.g. 0.5 means yield tags that contain
        half or more of the specified subset.
        :yield: the found tagsets
        """
        for tagset in self:
            if tagsubset.fraction_in(tagset) >= fuzz:
                yield tagset
