from geometry.vector import Vector
from geometry.point import Point

class Reflection:
    """Reflection([normal, [point]]) -> a reflection in the hyperplane
normal to the specified vector and passing through the specified
point.

    """
    def __init__(self, normal=(), point=()):
        v = Vector(*[x for x in normal])
        if v:
            v /= v.length()
        self._normal = v
        if v:
            if v.dot(point):
                p = Point(*[x for x in point])
            else:
                p = Point()         
        else:
            p = Point()
        #normalize the point to that closest to origin
        self._point = p#so apply works
        if p:
            p = self.apply((0,))/2
        self._point = p
        self._vec_norm = v.dot(v)

    def apply(self, point):
        """Apply the reflection to the specified point"""
        p = Point(*[x for x in point])
        v = (p - self.point)
        v = v - self.normal*(v.dot(self.normal)/self.normal.length())*2
        p = self.point + v
        return p

    @property
    def normal(self):
        """The normal of the plane of reflection"""
        return self._normal

    @property
    def point(self):
        """A point the plane of reflection passes through"""
        return self._point

    def dimension(self):
        return max(len(self.point), len(self.normal))

    def get_matrix_element(self, row, col):
        d = 0
        if row==col:
            d=1
        d -= 2*(self.normal[row]*self.normal[col])/self._vec_norm
        return d

    def __len__(self):
        return self.dimension()

    def __eq__(self, other):
        return isinstance(other, Reflection) and other.normal == self.normal and other.point == self.point
    
    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "Reflection(%s, %s)" % (str(self.normal), str(self.point))
    
    def __repr__(self):
        return "Reflection(%s, %s)" % (repr(self.normal), repr(self.point))
