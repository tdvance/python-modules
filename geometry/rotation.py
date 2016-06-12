class Rotation:
    """Rotation(reflection1, reflection2) a rotation about the hyperline
    that is the result of applying reflection1 and then reflection2.

    """
    def __init__(self, ref1, ref2):
        if not isinstance(ref1, Reflection) or not isinstance(ref2, Reflection):
            raise Exception("Arguments to Rotation constructor must be Reflection types")
        # TODO normalize
        self._ref1 = ref1
        self._ref2 = ref2

    def apply(self, point):
        p1 = self._ref1.apply(point)
        p2 = self._ref2.apply(p1)
        return p2

    @property
    def ref1(self):
        return self._ref1

    @property
    def ref2(self):
        return self._ref2

    def dimension(self):
        return max(len(self.ref1), len(self.ref2))

    def __len__(self):
        return self.dimension()

    def __eq__(self, other):
        return isinstance(other, Rotation) and other.ref1 == self.ref1 and other.ref2 == self.ref2
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return "Rotation(%s, %s)" % (str(self.ref1), str(self.ref2))
    
    def __repr__(self):
        return "Rotation(%s, %s)" % (repr(self.ref1), repr(self.ref2))
