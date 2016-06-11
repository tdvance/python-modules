import numbers

from algebra.monomial import Monomial
                               
class Poly:
    """A sparse multivariate polynomial type"""
    def __init__(self, *monomials):
        self._mdict = dict()
        for m in monomials:
            c = m.coef
            t = m.ftuple
            if not c:
                continue
            if t in self._mdict:
                self._mdict[t] += m
            else:
                self._mdict[t] = m
        l = list(self._mdict.values())
        l.sort()
        self._mtuple = tuple(l)

    def mtuple(self):
        """Return a sorted tuple of the monomials in this polynomial"""
        return self._mtuple
        
    def __str__(self):
        if not self.mtuple:
            return "0"
        for m in self.mtuple:
            if first:
                first=False
                result = str(m)
            else:
                c = m.coef
                if c > 0:
                    result += " + " + str(m)
                else:
                    result += " - " + str(-m)
        return result
                
            

        
        
        
                
            
            
            
            
