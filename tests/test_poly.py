#!/usr/bin/env python3

from poly import Poly


def check_poly_consistancy(f):
    assert(isinstance(f._coefs, tuple))
    assert(isinstance(f._var, str))
    if f._coefs:
        assert f._coefs[-1]

f1 = Poly(1,1,1,0,0,-1,-1,-2,-1,-1,0,0,1,1,1,1,1,1,0,0,-1,0,-1,0,-1,0,-1,0,-1,0,0,1,1,1,1,1,1,0,0,-1,-1,-2,-1,-1,0,0,1,1,1)

f2 = Poly(1,-1,0,0,0,1,-1,1,-1,0,1,-1,1,-1,1,0,-1,1,-1,1,0,0,0,-1,1)

f3 = Poly(1,-1,0,1,-1,0,1,0,-1,1,0,-1,1)
f4 = Poly(1,-1,0,1,-1,1,0,-1,1)
f5 = Poly(1,1,1,1,1,1,1)
f6 = Poly(1,1,1,1,1)
f7=Poly(1,1,1)
f8=Poly(-1,1)

assert(f1*f2*f3*f4*f5*f6*f7*f8  == (Poly.monomial(1,105)-1))
check_poly_consistancy(f1*f2*f3*f4*f5*f6*f7*f8)
