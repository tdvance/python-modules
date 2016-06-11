#!/usr/bin/env python3

from algebra.monomial import Monomial

def check_validity(m):
    if not m._coef:
        assert not m._fdict
    lastvar = ""
    for var, deg in m._ftuple:
        if lastvar:
            assert var >= lastvar
        lastvar = var
        assert m._fdict[var] == deg
    assert len(m._fdict) == len(m._ftuple)
    assert m.ftuple == m._ftuple
    assert m.coef == m._coef


m = Monomial(-1.23, x=2, y=1, z=0, w=3)
assert(str(m) == "-1.23w^3x^2y")
check_validity(m)
m = -m
assert(str(m) == "1.23w^3x^2y")
check_validity(m)
assert(repr(m) == "Monomial(1.23, {'w': 3, 'x': 2, 'y': 1})")


mm = Monomial(1, x=2, y=1, z=0, w=3)
assert(str(mm) == "w^3x^2y")
check_validity(mm)

mm += m
assert(str(mm) == "2.23w^3x^2y")
check_validity(mm)

m = Monomial(-1, x=2, y=1, z=0, w=3)
assert(str(m) == "-w^3x^2y")
check_validity(m)

mm = Monomial(0, x=2, y=1, z=0, w=3)
assert(str(mm) == "0")
check_validity(mm)

m *= mm
assert(str(m) == "0")
check_validity(m)

m = Monomial(-1.23, x=2, y=1, z=0, w=3)
mm = Monomial(2, x=1, z=2, t=3)
check_validity(mm)
m *= mm
check_validity(m)
assert(str(m) == "-2.46t^3w^3x^3yz^2")

m = m.get_monic()
check_validity(m)
assert(str(m) == "t^3w^3x^3yz^2")

m = Monomial(0, x=2, y=1, z=0, w=3)
m = m.get_monic()
check_validity(m)
assert(str(m) == "1")

m = Monomial(3)
check_validity(m)
assert(str(m) == "3")
m = m.get_monic()
check_validity(m)
assert(str(m) == "1")

