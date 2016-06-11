import numbers

class Monomial:
    """A multivariate monomial type"""
    def __init__(self, coef, **var_deg):
        self._coef = coef
        if coef:
            self._fdict=dict()
            for var in var_deg:
                deg = var_deg[var]
                if deg:
                    self._fdict[var] = deg
        else:
            self._fdict = dict()
        l = [var for var in self._fdict]
        l.sort()
        self._ftuple = tuple((var, self._fdict[var]) for var in l)

    @property
    def coef(self):
        """Return the coefficient of this monomial"""
        return self._coef

    @property
    def ftuple(self):
        """Return a sorted tuple of the variable-degree pairs of this polynomial"""
        return self._ftuple

    def get_monic(self):
        """Return a monoic monomial of like terms as this one"""
        return Monomial(1, **self._fdict)
    
    def __add__(self, other):
        """Add this monomial to another monomial or a scalar if possible"""
        if isinstance(other, Monomial):
            if self.ftuple != other.ftuple:
                raise NotImplementedError("Can only add like terms")
            c = self.coef + other.coef
            return Monomial(c, **self._fdict)
        elif isinstance(other, numbers.Number):
            if self._ftuple:
                raise NotImplementedError("Can only add like terms")
            return Monomial(self.coef + other)
        else:
            return other + self

    def __sub__(self, other):
        """Subtract from this monomial another monomial or a scalar if possible"""        
        return self + (-other)

    def __neg__(self):
        """Return the negation of this monomial"""
        c = - self.coef
        return Monomial(c, **self._fdict)

    def __pos__(self):
        return self
    
    def __mul__(self, other):
        """Return the product of this monomial and another monomial or a scalar"""
        if isinstance(other, Monomial):
            c = self.coef * other.coef
            d = dict(self._fdict)
            for var, deg in other._fdict.items():
                if var in d:
                    d[var] += deg
                else:
                    d[var] = deg
            return Monomial(c, **d)
        elif isinstance(other, numbers.Number):
            return Monomial(self.coef*other, **self._fdict)
        else:
            return other * self

    def  inv(self):
        """Return the reciprocal of this monomial if possible"""
        c = 1.0/self.coef
        d = dict()
        for var, deg in self._fdict.items():
            d[var] = -deg
        return Monomial(c, **d)

    def __truediv__(self, other):
        if isinstance(other, Monomial):
            return self * other.inv()
        elif isinstance(other, numbers.Number):
            return self / other
        elif hasattr(other, "inv"):
            return self * other.inv()
        else:
            raise NotImplementedError("division by " + type(other))

    def __bool__(self):
        return bool(self._coef)

    def __eq__(self, other):
        if not isinstance(other, Monomial):
            return False
        return self.coef == other.coef and self.ftuple == other.ftuple

    def __ne__(self, other):
        return not (self == other)

    def __pow__(self, value):
        c = self.coef**value
        d = dict()
        for var, deg in self.ftuple:
            d[var] = deg * value
        return Monomial(c, *d)
    
    def degree(self):
        """Return the total degree of the monomial, or -inf if it is the zero monomial"""
        if not self:
            return float('-inf')
        d = 0
        for var, deg in self.ftuple:
            d += deg
        return d


    def cmp_tlex(self, other):
        """Comparison function (signum) that uses total-degree, then revlex, then
        coef, for comparisson, return -1, 0, or 1, or raising
        NotImplementedError if other is a non-monomial or non-scalar
        incomparable with self.

        """
        if isinstance(other, Monomial):
            if self.degree() > other.degree():
                return 1
            elif self.degree() < other.degree():
                return -1
            i = len(self.ftuple) - 1
            j = len(other.ftuple) - 1
            while i >= 0 and j >= 0:
                v,d = self.ftuple[i]
                vv,dd = other.ftuple[j]
                if v > vv:
                    return 1
                elif v < vv:
                    return -1
                if d > dd:
                    return 1
                elif d < dd:
                    return -1
            if i>=0:
                return 1
            elif j >=0:
                return -1
            if self.coef > other.coef:
                return 1
            elif self.coef < other.coef:
                return -1
            else:
                return 0
        elif isinstance(other, numbers.Number):
            if self.degree() >0:
                return 1
            elif self.degree()<0 and other:
                return -1
            elif self.coef and not other:
                return 1
            elif self.degree()==0:
                if self.coef > other:
                    return 1
                elif self.coef < other:
                    return -1
                else:
                    return 0
            elif not self.coef and other:
                return -1
            elif not self.coef and not other:
                return 0
            else:
                assert("should be impossible to get here")
        elif other == self:
            return 0
        elif other < self:
            return 1
        else:
            return -1
            
    def __lt__(self, other):
        return self.cmp_tlex(other) < 0

    def __gt__(self, other):
        return self.cmp_tlex(other) > 0

    def __le__(self, other):
        return self.cmp_tlex(other) <= 0

    def __ge__(self, other):
        return self.cmp_tlex(other) >= 0        
    
    def apply(self, **values):
        """Apply this monomial to the specified variable substitutions and
        return the result, a possibly-constant monomial.

        """
        c = self.coef
        d = dict()
        for var, deg in self.ftuple:
            if var in values:
                c *= values[var]**deg
            else:
                d[var] = deg
        return Monomial(c, *d)
        
    def __str__(self):
        if not self._ftuple:
            return str(self._coef)
        if self._coef == 1:
            result = ""
        elif self._coef == -1:
            result = "-"
        else:
            result = str(self._coef)
        for (var, deg) in self._ftuple:
            result +=str(var)
            if deg != 1:
                result += "^"  + str(deg)
        return result

    def __repr__(self):
        result =  "Monomial(" + repr(self.coef) + ", " + "{"
        first = True
        for var, deg in self.ftuple:
            if first:
                first = False
            else:
                result += ", "
            result += repr(var) + ": " + repr(deg)
        result += "})"
        return result
