#!/usr/bin/env python3

import math

from geometry.point import Point
from geometry.vector import Vector

v = Vector(1,2,0,0)

assert str(v) == '(1.0, 2.0)'
assert repr(v) == 'Vector(1.0, 2.0)'
assert v[0] == 1
assert v[1] == 2
assert v[2] == 0
assert v[20] == 0
assert len(v) == 2

assert v + (1,) == Vector(2,2)
assert Point(1,3) + v == Point(2, 5)
assert v - Vector(1,3,5) == Vector(0, -1, -5)
assert -v == Vector(-1, -2)
assert v*5 == Vector(5, 10)
assert v/5 == Vector(0.2, 0.4)

assert v.translate((1,1,1)) == Vector(2,3,1)
assert v.scale(3) == Vector(3, 6)
assert v.length() == math.sqrt(5)
assert v.point(Point(3,4,5)) == Point(-2,-2,-5)
assert v.coordinates == (1,2)
for i in range(0, 20):
    assert v.get_coord(i) == v[i]
assert v.dimension == 2
assert v.dot(Vector(3,2)) == 7
