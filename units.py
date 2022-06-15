"""Class for defining physical base units"""

from .quantity import Quantity

from .exceptions import InconsistentUnitDefinition
from .exceptions import AttemptToAssignToUnit
from .exceptions import UndefinedUnit

from numpy import pi

_Prefixes = {
    'Y' : 10 ** 24,
    'Z' : 10 ** 21,
    'E' : 10 ** 18,
    'P' : 10 ** 15,
    'T' : 10 ** 12,
    'G' : 10 ** 9,
    'M' : 10 ** 6,
    'k' : 10 ** 3,
    'd' : 10 ** -1,
    'c' : 10 ** -2,
    'm' : 10 ** -3,
    'u' : 10 ** -6,
    'n' : 10 ** -9,
    'p' : 10 ** -12,
    'f' : 10 ** -15,
}

class Units:
    """Singleton class for accessing and defining base units

    The attributes of a Units instance are the currently defined
    physical unit quantities.  

    Example:

        u = Units()
        x = 3 * u.miles
        y = 4.2 * u.km
        KE = 15 * u.J
        torque = 52 * u.ft * u.lbf

    A subset of the units can be prefixed with SI style modifiers

        x = 3 * u.km
        y = 3000 * u.m

    Additional units may be defined using the add method
    """
    _Prefixable = set()
    _Instance = None

    def __new__(cls):
        if cls._Instance is None:
            cls._Instance = super(Units,cls).__new__(cls)
        return cls._Instance

    def __init__(self):
        self.add_base_units()
        self.add_angle_units()
        self.add_time_units()
        self.add_mks_units()
        self.add_imperial_units()

    @property
    def defined(self):
        """list of all currently defined units"""
        return tuple(self.__dict__.keys())

    @property
    def prefixable(self):
        """set of all currently defined prefixable units"""
        return Units._Prefixable

    def add(self, name, *args, can_prefix=False, **kwargs):
        value = 1
        unit = None
        if args:
            assert len(args) < 3
            if len(args) == 2:
                value, unit = args
            elif isinstance(args[0],Quantity):
                unit = args[0]
            else:
                value = args[0]

        unit = Quantity(value,unit,**kwargs)
        if name in self.__dict__:
            cur = self.__dict__[name]
            could_prefix = name in Units._Prefixable
            try:
                assert can_prefix == could_prefix
                assert unit == cur
                return cur
            except:
                raise InconsistentUnitDefinition(name,(cur,could_prefix),(unit,can_prefix))

        self.__dict__[name] = unit

        if can_prefix:
            Units._Prefixable.add(name)

        return unit

    def add_base_units(self):
        self.add('m',length=1,can_prefix=True)
        self.add('kg',mass=1)
        self.add('s',time=1,can_prefix=True)
        self.add('C',charge=1)
        self.add('K',temp=1)
        self.add('cd',illum=1)
        self.add('rad',angle=1)

        # synonyms
        self.add('g',0.001,self.kg,can_prefix=True)
        self.add('sec',self.s,can_prefix=True)
        self.add('coul',self.C,can_prefix=True)

    def add_angle_units(self):
        self.add('deg',pi/180,self.rad)
        self.add('cycle',360*self.deg)
        self.add('sr',self.rad**2)

    def add_time_units(self):
        self.add('min',60,self.sec)
        self.add('hr',60,self.min)
        self.add('day',24,self.hr)
        self.add('week',7,self.day)

    def add_mks_units(self):
        # mass
        self.add('tonne',1000,self.kg,can_prefix=True)

        # volumne
        self.add('ml', 1000, self.cm**3)
        self.add('L', 1000, self.ml, can_prefix=True)

        self.add('litre',self.L)
        self.add('liter',self.L)

        # derivative units
        self.add('Hz',1/self.sec,can_prefix=True)
        self.add('N',self.m*self.kg/self.sec**2,can_prefix=True)
        self.add('J',self.m*self.N,can_prefix=True)
        self.add('W',self.J/self.s,can_prefix=True)
        self.add('Pa',self.N/self.m**2,can_prefix=True)
        self.add('A',self.coul/self.sec,can_prefix=True)
        self.add('V',self.J/self.coul,can_prefix=True)
        self.add('F',self.coul/self.V,can_prefix=True)
        self.add('Ohm',self.V/self.A,can_prefix=True)
        self.add('lm',self.cd*self.sr)
        self.add('lx',self.lm/self.m**2)

        self.add('hertz',self.Hz)
        self.add('newton',self.N)
        self.add('joule',self.J)
        self.add('watt',self.W)
        self.add('pascal',self.Pa)
        self.add('amp',self.A)
        self.add('volt',self.V)
        self.add('farad',self.F)
        self.add('ohm',self.Ohm)
        self.add('lumen',self.lm)
        self.add('lux',self.lx)

    def add_imperial_units(self):
        # length
        self.add('inch', 2.54, self.cm)
        self.add('ft', 12, self.inch)
        self.add('foot', self.ft)
        self.add('feet', self.ft)
        self.add('yd', 3, self.ft)
        self.add('yard', self.yd)
        self.add('yards', self.yd)
        self.add('mi', 1760, self.yd)
        self.add('mile', self.mi)
        self.add('miles', self.mi)
        self.add('league', 3, self.mi)
        self.add('nmi', 1852, self.m)

        # area
        self.add('acre',4840, self.yd**2)

        # volume
        self.add('pt',28.875, self.inch**3)
        self.add('qt', 2, self.pt)
        self.add('gal', 4, self.qt)
        self.add('fl_oz', self.pt/16)

        self.add('pint',self.pt)
        self.add('quart',self.qt)
        self.add('gallon',self.gal)

        # weight
        self.add('oz', 28.375, self.g)
        self.add('lb', 16, self.oz)
        self.add('ton', 2000, self.lb)

        # force, energy, power
        self.add('lbf', 4.44822162, self.N)
        self.add('BTU', 1055.05585, self.J)        
        self.add('hp', 745.699872, self.W)


    def __setattr__(self, name, value):
        raise AttemptToAssignToUnit(name)

    def __getattr__(self, name):
        # unit not in dictionary, see if we can create it from
        #   a prefixable unit
        if len(name) > 1:
            try:
                prefix_factor = _Prefixes[name[:1]]
                base_unit = self.__dict__[name[1:]]
                assert name[1:] in Units._Prefixable
                return self.add(name, prefix_factor, base_unit)
            except:
                pass

        raise UndefinedUnit(name)
