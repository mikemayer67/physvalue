"""Class for expressing physical quantities"""

from .exceptions import IncompatibleUnits
from .exceptions import NotAnAngle

import math

class Quantity:
    """A physical quantity consistiting of a value and fundamental units

    An instance of the Quantity class can represent any physical measurement composed
    of 7 fundamental physical units (listed below).  It contains
    a scalar value and a tuple containing the exponents associated with each
    of the 7 fundamental units.

    The scalar value is set relative to the base units for each of the physical
    measurements.

    The fundamental measurements and associated base units are:
        - Length (meter)
        - Mass (kilogram)
        - Time (second)
        - Electric charge (coul)
        - Absolute temperature (Kelvin)
        - Intensity of lighth (candela)
        - Angle (rad)

    Constructor:

    Thare are three means for constructing a Quantity value:

    - value and fundamental unit exponents

        Args:
            value (number): numeric value in MKS units
            length (optional): exponent on the length component
            mass (optional): exponent on the mass component
            time (optional): exponent on the time component
            charge (optional): exponent on the electric charge component
            temp (optional): exponent on the absolute temperature component
            illum (optional): exponent on the light intensity component
            angle (optional): exponent on the angle quantity component

    - scalar and base quantity

        Args:
            value (number): amount by which to scale the base quantity
            unit (Quantity): base value and units

    - scalar and tuple of unit exponents

        Args:
            value (number): numeric value in MKS unit
            unit (tuple): exponent values as listed above

    """
    __slots__ = ('value','unit')


    def __new__(cls, value=1, unit=None, 
            *, 
            length=0,mass=0,time=0,charge=0,temp=0,illum=0,angle=0):

        if unit is None:
            unit = (length,mass,time,charge,temp,illum,angle)
        elif isinstance(unit,Quantity):
            unit = unit.unit

        if [t for t in unit if t != 0]:
            return super(Quantity,cls).__new__(cls)
        else:
            return value


    def __init__(self, value=1, unit=None, 
            *, 
            length=0,mass=0,time=0,charge=0,temp=0,illum=0,angle=0):
        if unit is None:
            self.unit = (length,mass,time,charge,temp,illum,angle)
            self.value = value
        elif isinstance(unit,Quantity):
            self.unit = unit.unit
            self.value = value * unit.value
        elif len(unit) == 7:
            self.unit = tuple(unit)
            self.value = value
        else:
            raise TypeError("unit value must be Quantity of tuple of length 8")

    def compatible(self,other):
        try:
            return self.unit == other.unit
        except Exception as e:
            return False

    def assert_compatible(self,other):
        if not self.compatible(other):
            raise IncompatibleUnits(self,other)


    def __abs__(self):
        return Quantity(abs(self.value), unit=self.unit)

    def __add__(self,other):
        self.assert_compatible(other)
        return Quantity(self.value + other.value, unit=self.unit)

    __radd__ = __add__

    def __neg__(self):
        return Quantity(-self.value, unit=self.unit)
    
    def __sub__(self,other):
        self.assert_compatible(other)
        return Quantity(self.value - other.value, unit=self.unit)

    def __rsub__(self,other):
        self.assert_compatible(other)
        return Quantity(other.value - self.value, unit=self.unit)

    def __mul__(self,other):
        if isinstance(other,Quantity):
            unit = tuple(a + b for a,b in zip(self.unit,other.unit))
            product = Quantity(self.value * other.value, unit=unit)
        else:
            product = Quantity(self.value * other, unit=self.unit)

        return product

    __rmul__ = __mul__

    def invert(self):
        unit = tuple(-t for t in self.unit)
        return Quantity(1/self.value, unit=unit)

    def __truediv__(self,other):
        if isinstance(other,Quantity):
            unit = tuple(a - b for a,b in zip(self.unit,other.unit))
            quotient = Quantity(self.value / other.value, unit=unit)
        else:
            quotient = Quantity(self.value / other, unit=self.unit)

        return quotient

    def __rtruediv__(self,other):
        if isinstance(other,Quantity):
            unit = tuple(b-a for a,b in zip(self.unit,other.unit))
            quotient = Quantity(other.value / self.value, unit=unit)
        else:
            unit = tuple(-t for t in self.unit)
            quotient = Quantity(other / self.value, unit=unit)

        return quotient

    def __floordiv__(self,other):
        if isinstance(other,Quantity):
            unit = tuple(a - b for a,b in zip(self.unit,other.unit))
            quotient = Quantity(self.value // other.value, unit=unit)
        else:
            quotient = Quantity(self.value // other, unit=self.unit)

        return quotient

    def __rfloordiv__(self,other):
        if isinstance(other,Quantity):
            unit = tuple(b-a for a,b in zip(self.unit,other.unit))
            quotient = Quantity(other.value // self.value, unit=unit)
        else:
            unit = tuple(-t for t in self.unit)
            quotient = Quantity(other // self.value, unit=unit)

        return quotient

    def __pow__(self,n):
        unit = tuple(n*t for t in self.unit)
        return Quantity( self.value ** n, unit=unit )

    def root(self,n):
        unit = tuple(t/n for t in self.unit)
        return Quantity( self.value ** (1/n), unit=unit )

    def sqrt(self):
        return self.root(2)


    def __eq__(self, other):
        self.assert_compatible(other)
        return (self.value == other.value) and (self.unit == other.unit)
 
    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        self.assert_compatible(other)
        return self.value < other.value

    def __le__(self, other):
        self.assert_compatible(other)
        return self.value <= other.value

    def __gt__(self, other):
        self.assert_compatible(other)
        return self.value > other.value

    def __ge__(self, other):
        self.assert_compatible(other)
        return self.value >= other.value

    def __nonzero__(self):
        return True if self.value else False
    __bool__ = __nonzero__

    def __repr__(self):
        keys = ('length','mass','time','charge','temp','illum','angle')
        return (f"Quantity({self.value},"
                + ",".join(f"{n}={e}" for n,e in zip(keys,self.unit) if e)
                + ",)")

    def __str__(self):
        names = ('m','kg','s','C','K','cd','rad')
        num = " ".join(f"{n}" if e==1 else f"{n}^{e}" for n,e in zip(names,self.unit) if e>0)
        den = " ".join(f"{n}" if e==-1 else f"{n}^{-e}" for n,e in zip(names,self.unit) if e<0)

        if num:
            if den:
                return f"{self.value}[{num}/{den}]"
            else:
                return f"{self.value}[{num}]"
        elif den:
            return f"{self.value}[1/{den}]"
        else:
            return f"{self.value}"

    def __getattr__(self,name):
        from pval import units as u
        try:
            unit = getattr(u,name)
            self.assert_compatible(unit)
            return self/unit
        except Exception as e:
            raise AttributeError(f"{e}")

    def __float__(self):
        if not self.compatible(Quantity(1,angle=1)):
            raise NotAnAngle('float',self)
        return self.value

    # the following are to support numpy trig functions
    def sin(self):
        if not self.compatible(Quantity(1,angle=1)):
            raise NotAnAngle('sin',self)
        return math.sin(self.value)

    def cos(self):
        if not self.compatible(Quantity(1,angle=1)):
            raise NotAnAngle('sin',self)
        return math.cos(self.value)

    def tan(self):
        if not self.compatible(Quantity(1,angle=1)):
            raise NotAnAngle('sin',self)
        return math.tan(self.value)

