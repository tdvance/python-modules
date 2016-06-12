import geometry

class Point:
    """Point([x [, y [,z ...]]]) -> a point in a space of any number of
    dimensions.  Coordinates in dimensions not specified are taken as
    zero.

    """
    def __init__(self, *args):
        coords = [float(x) for x in args]
        while coords and not coords[-1]:
            coords.pop()
        self._coords = tuple(coords)
        
    def translate(self, vector):
        """Return a new point that is this point translated by the vector"""
        coords = []
        for i in range(max(len(self), len(vector))):
            coords.append(self[i] + Point._get_coord(vector, i))
        return Point(*coords)

    def rotate(self, rotation):
        """Return a new point rotated by the specified rotation"""
        return rotation.apply(self)

    def scale(self, amount, center=()):
        """Return a new point scaled from the specified center point by the
scalar amount"""
        coords = []
        for i in range(max(len(self), len(center))):
            c = Point._get_coord(center, i)
            coords.append((self[i] - c)*amount + c)
        return Point(*coords)
    
    def distance(self, center=()):
        """Return the Euclidean distance of this point from the specified
center point"""
        v = self.vector(center)
        return v.length()

    def vector(self, center=()):
        """Return the vector that would translate the specified center point to this point"""
        coords = []
        for i in range(max(len(self), len(center))):
            coords.append(self[i] - Point._get_coord(center, i))
        return geometry.vector.Vector(*coords)

    @property
    def coordinates(self):
        """Return the tuple of coordinates of this point, ignoring trailing zeros"""
        return self._coords

    def get_coord(self, i):
        """Get the i coordinate of this point.  Return 0 if past the end."""        
        return Point._get_coord(self.coordinates, i)

    @property
    def ambient_dimension(self):
        """Return the dimension of the space this point resides in, ignoring
trailing zeros in coordinates.  For example, Point(1,2,3) is in
3-dimensional space, and Point(1,0,2,0,-1,0,0) is in 5-dimensional
space.  The origin has ambient dimension zero.

        """
        return len(self.coordinates)

    def __str__(self):
        return str(self.coordinates)

    def __repr__(self):
        return "Point"+str(self.coordinates)

    def __getitem__(self, i):
        return self.get_coord(i)

    def __len__(self):
        return self.ambient_dimension

    @staticmethod
    def _get_coord(v, i):
        if i>=len(v):
            return 0
        return v[i]
        
    def __add__(self, vector):
        return self.translate(vector)

    def __sub__(self, other):
        if isinstance(other, Point):
            return self.vector(other)
        else: #treat other as vector
            coords = []
            for i in range(max(len(self), len(other))):
                coords.append(self[i] - Point._get_coord(other, i))
            return Point(*coords)

    def __neg__(self):
        return self.scale(-1)

    def __mul__(self, amount):
        return self.scale(amount)

    def __truediv__(self, amount):
        return self.scale(1.0/amount)
    
    def __eq__(self, other):
        return isinstance(other, Point) and self.coordinates == other.coordinates

    def __iter__(self):
        return iter(self.coordinates)    

    def __ne__(self, other):
        return not self == other    
