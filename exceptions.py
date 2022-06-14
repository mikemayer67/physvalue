"""pval exception classes"""

class IncompatibleUnits(TypeError):
  def __init__(self,a,b):
      a_unit = a.unit if hasattr(a,"unit") else "dimensionless"
      b_unit = b.unit if hasattr(b,"unit") else "dimensionless"
      TypeError.__init__(self,f"Operands have a different fundamental measure: {a_unit} vs {b_unit}")

class InconsistentUnitDefinition(RuntimeError):
    def __init__(self,name,old_def,new_def):
        RuntimeError.__init__(self,
            f"Base unit {name} was previously defined differently:\n"
            + f"old: {old_def}\n"
            + f"new: {new_def}")

class AttemptToAssignToUnit(RuntimeError):
    def __init__(self,name):
        RuntimeError.__init__(self,
            f"Cannot directly assign value to units.{name}" )
