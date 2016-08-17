from util.tag import Tag


class TagSet:
    def __init__(self, *tags):
        self._tags = dict()
        for tag in tags:
            self._tags[tag.key] = tag

    def __contains__(self, tag):
        return tag.key in self._tags and self._tags[tag.key] == tag

    def contains_key(self, tag):
        if isinstance(tag, str):
            return Tag.normalize(tag) in self._tags
        return tag.key in self._tags

    def get_from_key(self, tag):
        if isinstance(tag, str):
            return self._tags[Tag.normalize(tag)]
        return self._tags[tag.key]

    def is_subset_of(self, tags):
        for t in self:
            if t not in tags:
                return False
        return True

    def fraction_in(self, tags):
        total = len(self._tags)
        if (total == 0):
            return 1.0
        count = 0.0
        for t in self:
            if t in tags:
                count += 1
        return float(count) / float(total)

    def __iter__(self):
        return iter(self._tags.values())

    def __len__(self):
        return len(self._tags)

    def __str__(self):
        l = [str(x) for x in self]
        l.sort()
        return '{' + ', '.join(l) + '}'
