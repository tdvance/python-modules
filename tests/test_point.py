#!/usr/bin/env python3

from geometry.point import Point
from geometry.vector import Vector

p = Point(1,2,0,0)

assert str(p) == '(1.0, 2.0)'
assert repr(p) == 'Point(1.0, 2.0)'
assert p[0] == 1
assert p[1] == 2
assert p[2] == 0
assert p[20] == 0
assert len(p) == 2

assert p + (1,) == Point(2,2)
assert p + Point(1,3) == Point(2, 5)
assert p - Point(1,3,5) == Vector(0, -1, -5)
assert -p == Point(-1, -2)
assert p*5 == Point(5, 10)
assert p/5 == Point(0.2, 0.4)

assert p.translate((1,1,1)) == Point(2,3,1)
assert p.scale(3, Point(1,1)) == Point(1,4)
assert p.distance(Point(4, 6))==5
assert p.vector() == Vector(1,2)
assert p.coordinates == (1,2)
for i in range(0, 20):
    assert p.get_coord(i) == p[i]
assert p.ambient_dimension == 2
