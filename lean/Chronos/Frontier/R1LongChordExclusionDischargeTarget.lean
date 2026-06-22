import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract

namespace Chronos
namespace Frontier

/--
Discharge target for the `r1LongChordExclusion` field of the native-map input
contract.

This records the weakest current target for long-chord exclusion: a concrete
source object, a named proposition, and evidence for that proposition. It does
not supply such evidence for any concrete source object.
-/
structure R1LongChordExclusionDischargeTarget (D : R1SemanticData) : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  r1LongChordExclusion : Prop
  longChordExclusionEvidence : r1LongChordExclusion


/--
The concrete Newstein/FGL source object supplies a concrete long-chord discharge
target by taking the already-proved semantic long-chord theorem as the named
target proposition.
-/
def r1_concrete_newstein_fgl_source_long_chord_discharge_target
    (x : R1ConcreteNewsteinFGLGeometrySourceObject) :
    R1LongChordExclusionDischargeTarget R1ConcreteNativeSafeSemanticData where
  source := x
  r1LongChordExclusion :=
    R1LongChordExclusionTheorem R1ConcreteNativeSafeSemanticData
  longChordExclusionEvidence :=
    r1_concrete_native_safe_long_chord_exclusion_from_concrete_newstein_fgl_source x

/--
The active boundary is that long-chord exclusion has not yet been discharged for
the concrete Newstein/FGL source object.
-/
def r1_long_chord_exclusion_discharge_target_boundary : String :=
  "NO_DISCHARGED_R1_LONG_CHORD_EXCLUSION_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT"

end Frontier
end Chronos
