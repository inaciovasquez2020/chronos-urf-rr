import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract
import Chronos.Frontier.FourBridgesRegistryIntegration

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
An external Four Bridges source conditionally supplies the uniform local-type
capacity discharge target for the concrete Newstein/FGL source object.

This does not install an active bridge registry instance and does not prove
unconditional native R3 closure.
-/
def r1_uniform_local_type_capacity_discharge_target_from_4bS
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (bridges : FourBridgesSource) :
    R1UniformLocalTypeCapacityDischargeTarget where
  source := x
  r1UniformLocalTypeCapacity :=
    UniformLocalTypeCapacityProofTarget
  uniformLocalTypeCapacityEvidence :=
    R3_from_4bS bridges

theorem r1_uniform_target_from_4bS_eq
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (bridges : FourBridgesSource) :
    (r1_uniform_local_type_capacity_discharge_target_from_4bS x bridges).r1UniformLocalTypeCapacity =
      UniformLocalTypeCapacityProofTarget := by
  rfl

/--
The active boundary is that uniform local-type capacity has not yet been
discharged for the concrete Newstein/FGL source object.
-/
def r1_uniform_local_type_capacity_discharge_target_boundary : String :=
  "NO_DISCHARGED_R1_UNIFORM_LOCAL_TYPE_CAPACITY_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT"

end Frontier
end Chronos
