import math

from geometry.point import Point

class Vector:
    """Vector([x [, y [,z ...]]]) -> a vector (offset between two points)
    in a space of any number of dimensions.  Coordinates in dimensions
    not specified are taken as zero.

    """
    def __init__(self, *args):
        coords = [float(x) for x in args]
        while coords and not coords[-1]:
            coords.pop()
        self._coords = tuple(coords)

    def translate(self, other):
        """Return a new vector that is this vector translated by the other
        vector (parallelogram rule)
        
        """
        coords = []
        for i in range(max(len(self), len(other))):
            coords.append(self[i] + Point._get_coord(other, i))
        return Vector(*coords)        

    def scale(self, amount):
        """Return a new vector scaled by the scalar amount"""
        coords = []
        for x in self:
            coords.append(x*amount)
        return Vector(*coords)

    def dot(self, other):
        """Return the dot product of this vector with the other vector"""
        d = 0
        for i in range(max(len(self), len(other))):
            d += self[i]*Point._get_coord(other, i)
        return d
    
    def length(self):
        """Return the Euclidean length of this vector"""
        return math.sqrt(self.dot(self))

    def point(self, center=()):
        """Return the point that is the specified center point translated by
        this vector

        """
        coords = []
        for i in range(max(len(self), len(center))):
            coords.append(self[i] - Point._get_coord(center, i))
        return Point(*coords)
    
    @property
    def coordinates(self):
        """Return the tuple of coordinates of this vector, ignoring trailing zeros"""
        return self._coords

    def get_coord(self, i):
        """Get the i coordinate of this vector.  Return 0 if past the end."""
        return Point._get_coord(self.coordinates, i)

    @property
    def dimension(self):
        """Return the dimensionality of this vector, ignoring trailing zeros
in coordinates.  For example, Vector(1,2,3) is in 3-dimensional space,
and vector(1,0,2,0,-1,0,0) is in 5-dimensional space.  The zero vector
has dimensionality zero.

        """
        return len(self.coordinates)

    def __str__(self):
        return str(self.coordinates)

    def __repr__(self):
        return "Vector"+str(self.coordinates)

    def __getitem__(self, i):
        return self.get_coord(i)

    def __len__(self):
        return self.dimension

    def __add__(self, other):
        if isinstance(other, Point):
            return self.point(other)# return a point
        else:
            return self.translate(other)# return a vector

    def __sub__(self, other):
        coords = []
        for i in range(max(len(self), len(other))):
            coords.append(self[i] - Point._get_coord(other, i))
        return Vector(*coords)

    def __neg__(self):
        return self.scale(-1)

    def __mul__(self, amount):
        return self.scale(amount)

    def __truediv__(self, amount):
        return self.scale(1.0/amount)
    
    def __eq__(self, other):
        return isinstance(other, Vector) and self.coordinates == other.coordinates

    def __iter__(self):
        return iter(self.coordinates)

    def __ne__(self, other):
        return not self == other
