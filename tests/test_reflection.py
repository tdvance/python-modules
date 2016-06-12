#!/usr/bin/env python3

import math

from geometry.point import Point
from geometry.vector import Vector
from geometry.reflection import Reflection

xy = Reflection(Vector(0,0,1), Point(0,0,0))
xz = Reflection(Vector(0,1,0), Point(0,0,0))
yz = Reflection(Vector(1,0,0), Point(0,0,0))


p = Point(1,2,3)

assert xy.apply(p) == Point(1,2,-3)
assert xz.apply(p) == Point(1,-2,3)
assert yz.apply(p) == Point(-1,2,3)

xy5 = Reflection(Vector(0,0,7), Point(1,2,5))
assert xy5.apply(p) == Point(1,2,7)
assert xy5.point == Point(0,0,5)
assert xy5.normal == Vector(0,0,1)

mat = [[xy.get_matrix_element(row, col) for row in range(xy.dimension())] for col in range(xy.dimension())]

assert mat == [[1,0,0],[0,1,0],[0,0,-1]]

assert xy != yz
assert xy5 == Reflection(Vector(0,0,3), Point(3,4,5))
