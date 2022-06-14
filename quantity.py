"""Core class for expressing a physical quantity

An instance of the Quantity class can represent any physical measurement composed
of the 7 fundamental physical measurements (listed below).  It contains
a scalar value and a tuple containing the exponents associated with each
of the 7 fundamental measurements.

The scalar value is set relative to the base units for each of the physical
measurements.

The fundamental measurements and associated base units are:
    - Length (meter)
    - Mass (kilogram)
    - Time (second)
    - Electric current (ampere)
    - Absolute temperature (Kelvin)
    - Intensity of lighth (candela)
    - Quantity of substance (mole)
"""

from .exceptions import InvalidUnitDefinition
from .exceptions import IncompatibleUnits

class Quantity:
    __slots__ = ('value','unit')


    def __new__(cls, value=1, *, unit=None, m=0, kg=0, sec=0, amp=0, K=0, cand=0, mol=0):
        if unit:
            if isinstance(unit,Quantity):
                unit = unit.unit
            elif type(unit) not in (list,tuple):
                raise InvalidUnitDefinition(unit)
            elif len(unit) != 7:
                raise InvalidUnitDefinition(unit)
        else:
            unit = (m,kg,sec,amp,K,cand,mol)

        if [t for t in unit if t != 0]:
            return super(Quantity,cls).__new__(cls)
        else:
            return value


    def __init__(self, value=1, *, unit=None, m=0, kg=0, sec=0, amp=0, K=0, cand=0, mol=0):
        if unit:
            if isinstance(unit,Quantity):
                value = value * unit.value
                unit = unit.unit
            elif type(unit) is list:
                unit = tuple(unit)
        else:
            unit = (m,kg,sec,amp,K,cand,mol)

        self.value = value
        self.unit = unit

    def compatible(self,other):
        try:
            return self.unit == other.unit
        except Exception as e:
            return False

    def __abs__(self):
        return Quantity(abs(self.value), unit=self.unit)

    def __add__(self,other):
        if not self.compatible(other):
            raise IncompatibleUnits(self,other)
        return Quantity(self.value + other.value, unit=self.unit)

    __radd__ = __add__

    def __neg__(self):
        return Quantity(-self.value, unit=self.unit)
    
    def __sub__(self,other):
        if not self.compatible(other):
            raise IncompatibleUnits(self,other)
        return Quantity(self.value - other.value, unit=self.unit)

    def __rsub__(self,other):
        if not self.compatible(other):
            raise IncompatibleUnits(self,other)
        return Quantity(other.value - self.value, unit=self.unit)

    def __mul__(self,other):
        if isinstance(self,Quantity):
            if isinstance(other,Quantity):
                unit = tuple(a + b for a,b in zip(self.unit,other.unit))
                product = Quantity(self.value * other.value, unit=unit)
            else:
                product = Quantity(self.value * other, unit=self.unit)
        elif isinstance(other,Quantity):
            product = Quantity(value * other.value, unit=other.unit)
        else:
            product = self * other

        return product

    __rmul__ = __mul__

    def invert(self):
        unit = tuple(-t for t in self.unit)
        return Quantity(1/self.value, unit=unit)

    def __truediv__(self,other):
        if isinstance(self,Quantity):
            if isinstance(other,Quantity):
                unit = tuple(a - b for a,b in zip(self.unit,other.unit))
                quotient = Quantity(self.value / other.value, unit=unit)
            else:
                quotient = Quantity(self.value / other, unit=self.unit)
        elif isinstance(other,Quantity):
            unit = tuple(-t for t in other.unit)
            quotient = Quantity(self / other.value, unit=unit)
        else:
            quotient = self / other

        return quotient

    def __rtruediv__(self,other):
        if isinstance(self,Quantity):
            if isinstance(other,Quantity):
                unit = tuple(b-a for a,b in zip(self.unit,other.unit))
                quotient = Quantity(other.value / self.value, unit=unit)
            else:
                unit = tuple(-t for t in self.unit)
                quotient = Quantity(other / self.value, unit=unit)
        elif isinstance(other,Quantity):
            quotient = Quantity(other / self.value, unit=other.unit)
        else:
            quotient = other / self

        return quotient

    def __floordiv__(self,other):
        if isinstance(self,Quantity):
            if isinstance(other,Quantity):
                unit = tuple(a - b for a,b in zip(self.unit,other.unit))
                quotient = Quantity(self.value // other.value, unit=unit)
            else:
                quotient = Quantity(self.value // other, unit=self.unit)
        elif isinstance(other,Quantity):
            unit = tuple(-t for t in other.unit)
            quotient = Quantity(self // other.value, unit=unit)
        else:
            quotient = self // other

        return quotient

    def __rfloordiv__(self,other):
        if isinstance(self,Quantity):
            if isinstance(other,Quantity):
                unit = tuple(b-a for a,b in zip(self.unit,other.unit))
                quotient = Quantity(other.value // self.value, unit=unit)
            else:
                unit = tuple(-t for t in self.unit)
                quotient = Quantity(other // self.value, unit=unit)
        elif isinstance(other,Quantity):
            quotient = Quantity(other // self.value, unit=other.unit)
        else:
            quotient = other // self

        return quotient


#     def __eq__(self, other):
#         if not compatible(self.unit, other.unit):
#             return False
#         else:
#             return cmp(self, other) == 0
# 
#     def __ne__(self, other):
#         return not self == other
# 
#     def __lt__(self, other):
#         self._ensure_same_type(other)
#         return self.num * self.unit.squeeze() < \
#                 other.num * other.unit.squeeze()
# 
#     def __cmp__(self, other):
#         self._ensure_same_type(other)
#         return cmp(self.num * self.unit.squeeze(),
#                    other.num * other.unit.squeeze())
# 
#     def __le__(self, other):
#         return self == other or self < other
# 
#     def __complex__(self):
#         return complex(self.num)
# 
#     def __float__(self):
#         return float(self.num)
# 
#     def __index__(self):
#         return self.num
# 
#     def __hex__(self):
#         """Backwards-compatibility with Python <= 2.7."""
#         return hex(self.__index__())
# 
#     def __int__(self):
#         return int(self.num)
# 
#     def __neg__(self):
#         return Quantity(-self.num, self.unit)
# 
#     def __nonzero__(self):
#         return bool(self.num)
#     __bool__ = __nonzero__
# 
#     def __oct__(self):
#         return oct(self.num)
# 
#     def __pos__(self):
#         return self.num > 0
# 
#     def __pow__(self, exponent):
#         return Quantity(self.num ** exponent, self.unit ** exponent)
# 
#     def __str__(self):
#         num = self.num
#         if not self.unit.str_includes_multiplier():
#             num *= self.unit.squeeze()
#         return '%0.2f %s' % (num, self.unit)
# 
#     def __repr__(self):
#         return ("Quantity(" +
#                 ", ".join([repr(x) for x in [self.num, self.unit]]) +
#                 ")")
# 
