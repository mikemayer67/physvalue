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
        else:
            if isinstance(other,Quantity):
                product = Quantity(self.value * other, unit=self.unit)
            else:
                product = self * other

        return product

    __rmul__ = __mul__
