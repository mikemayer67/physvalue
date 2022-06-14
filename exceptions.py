"""pval exception classes"""

class PhysValueError(Exception):
    pass

class InvalidUnitDefinition(TypeError):
  def __init__(self,e):
    TypeError.__init__(self,f"Expected PhysicalQuantity or tuple of 7 values, got {e}")

class IncompatibleUnits(TypeError):
  def __init__(self,a,b):
      a_unit = a.unit if hasattr(a,"unit") else "dimensionless"
      b_unit = b.unit if hasattr(b,"unit") else "dimensionless"
      TypeError.__init__(self,f"Operands have a different fundamental measure: {a_unit} vs {b_unit}")
