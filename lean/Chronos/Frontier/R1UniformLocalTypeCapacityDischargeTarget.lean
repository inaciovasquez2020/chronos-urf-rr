import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract

namespace Chronos
namespace Frontier

/--
Discharge target for the `r1UniformLocalTypeCapacity` field of the native-map
input contract.

This records the weakest current target for uniform local-type capacity: a
concrete source object, a named proposition, and evidence for that proposition.
It does not supply such evidence for any concrete source object.
-/
structure R1UniformLocalTypeCapacityDischargeTarget : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  r1UniformLocalTypeCapacity : Prop
  uniformLocalTypeCapacityEvidence : r1UniformLocalTypeCapacity

/--
The active boundary is that uniform local-type capacity has not yet been
discharged for the concrete Newstein/FGL source object.
-/
def r1_uniform_local_type_capacity_discharge_target_boundary : String :=
  "NO_DISCHARGED_R1_UNIFORM_LOCAL_TYPE_CAPACITY_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT"

end Frontier
end Chronos
