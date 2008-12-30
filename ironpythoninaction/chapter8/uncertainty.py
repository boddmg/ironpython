class Uncertainty(object):
    def __init__(self, value, spread):
        self.value = value
        self.spread = spread

    def __add__(self, other):
        if isinstance(other, Uncertainty):
            value = self.value + other.value
            spread = self.spread + other.spread
            return Uncertainty(mag, spread)
        return Uncertainty(self.value + other, self.spread)

    def __radd__(self, other): 
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, Uncertainty):
            value = self.value * other.value
            spread = (
                self.spread * other.spread +
                self.value * other.spread +
                self.spread * other.value
            )
            return Uncertainty(value, spread)
        return Uncertainty(self.value * other, self.spread * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return 'Uncertainty(%s, %s)' % (self.value, self.spread)

    def __str__(self):
        return u"%s\u00b1%s" % (self.value, self.spread) 
