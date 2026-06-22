import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract

namespace Chronos
namespace Frontier

/--
Discharge target for the `r1SourceToNativeCompatibility` field of the native-map
input contract.

This records the weakest current target for source-to-native compatibility: a
concrete source object, a named proposition, and evidence for that proposition.
It does not supply such evidence for any concrete source object.
-/
structure R1SourceToNativeCompatibilityDischargeTarget : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  r1SourceToNativeCompatibility : Prop
  sourceToNativeCompatibilityEvidence : r1SourceToNativeCompatibility

/--
The active boundary is that source-to-native compatibility has not yet been
discharged for the concrete Newstein/FGL source object.
-/
def r1_source_to_native_compatibility_discharge_target_boundary : String :=
  "NO_DISCHARGED_R1_SOURCE_TO_NATIVE_COMPATIBILITY_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT"

end Frontier
end Chronos
