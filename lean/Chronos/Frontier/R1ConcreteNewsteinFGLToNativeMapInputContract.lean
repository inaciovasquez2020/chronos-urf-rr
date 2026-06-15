import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget

/--
Weakest current input contract for a future native construction map from the
concrete Newstein/FGL source object to the native R1 geometry input object.

This contract is intentionally non-vacuous: it requires evidence fields for the
named geometric ingredients before any construction map may be introduced.
-/
structure R1ConcreteNewsteinFGLToNativeMapInputContract : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  r1LongChordExclusion : Prop
  r1DiameterSeparationFillingObstruction : Prop
  r1UniformLocalTypeCapacity : Prop
  r1SourceToNativeCompatibility : Prop
  longChordExclusionEvidence : r1LongChordExclusion
  diameterSeparationFillingObstructionEvidence : r1DiameterSeparationFillingObstruction
  uniformLocalTypeCapacityEvidence : r1UniformLocalTypeCapacity
  sourceToNativeCompatibilityEvidence : r1SourceToNativeCompatibility

/--
The active boundary is that the input contract has not yet been discharged for
concrete Newstein/FGL geometry.
-/
def r1_concrete_newstein_fgl_to_native_map_input_contract_boundary : String :=
  "NO_DISCHARGED_INPUT_CONTRACT_FOR_NATIVE_CONSTRUCTION_MAP"
