"""Class for defining physical base units"""

from .quantity import Quantity

from .exceptions import InconsistentUnitDefinition
from .exceptions import AttemptToAssignToUnit

class Units:
    """Singleton class for accessing and defining base units
    """
    _Registry = {}
    _Instance = None

    def __new__(cls):
        if cls._Instance is None:
            cls._Instance = super(Units,cls).__new__(cls)
        return cls._Instance

    def __init__(self):
        Units.add_mks_units()
        for k,v in Units._Registry.items():
            self.__dict__[k] = v[0]

    @classmethod
    def add(cls, name, value, unit=None, *, can_prefix=False, **kwargs):
        unit = Quantity(value,unit,**kwargs)
        if name in cls._Registry:
            cur = cls._Registry[name]
            if unit != cur[0] or can_prefix != cur[1]:
                raise InconsistentUnitDefinition(name,cur,(unit,can_prefix))
        else:
            cls._Registry[name] = (unit,can_prefix)

    def __setattr__(self, name, value):
        raise AttemptToAssignToUnit(name)

    @classmethod
    def add_mks_units(cls):
        # base units
        cls.add('m',1,m=1,can_prefix=True)
        cls.add('kg',1,kg=1)
        cls.add('s',1,s=1,can_prefix=True)
        cls.add('C',1,C=1,can_prefix=True)
        cls.add('K',1,K=1)
        cls.add('cand',1,cand=1)
        cls.add('mol',1,mol=1)

        # related units and synonyms
        cls.add('g',0.001,kg=1,can_prefix=True)
        cls.add('sec',1,s=1,can_prefix=True)
        cls.add('coul',1,C=1,can_prefix=True)

