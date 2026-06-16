import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract

/--
Discharge target for the `r1LongChordExclusion` field of the native-map input
contract.

This records the weakest current target for long-chord exclusion: a concrete
source object, a named proposition, and evidence for that proposition. It does
not supply such evidence for any concrete source object.
-/
structure R1LongChordExclusionDischargeTarget : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  r1LongChordExclusion : Prop
  longChordExclusionEvidence : r1LongChordExclusion

/--
The active boundary is that long-chord exclusion has not yet been discharged for
the concrete Newstein/FGL source object.
-/
def r1_long_chord_exclusion_discharge_target_boundary : String :=
  "NO_DISCHARGED_R1_LONG_CHORD_EXCLUSION_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT"
