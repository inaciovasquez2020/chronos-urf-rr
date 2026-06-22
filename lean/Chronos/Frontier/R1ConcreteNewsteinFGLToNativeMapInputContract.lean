import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget

namespace Chronos
namespace Frontier

/--
Weakest current input contract for a future native construction map from the
concrete Newstein/FGL source object to the native R1 geometry input object.

This contract is intentionally non-vacuous: it requires evidence fields for the
named geometric ingredients before any construction map may be introduced.
-/
structure R1ConcreteNewsteinFGLToNativeMapInputContract (D : R1SemanticData) : Type where
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
The long-chord component of the native-map input contract, isolated from the
still-missing diameter-separation, uniform-capacity, and compatibility fields.
-/
structure R1ConcreteNewsteinFGLToNativeMapLongChordInputField (D : R1SemanticData) : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  r1LongChordExclusion : Prop
  longChordExclusionEvidence : r1LongChordExclusion

/--
Any full native-map input contract exposes its long-chord component.
-/
def r1_concrete_newstein_fgl_to_native_map_input_contract_long_chord_field
    (x : R1ConcreteNewsteinFGLToNativeMapInputContract D) :
    R1ConcreteNewsteinFGLToNativeMapLongChordInputField D where
  source := x.source
  r1LongChordExclusion := x.r1LongChordExclusion
  longChordExclusionEvidence := x.longChordExclusionEvidence

/--
The active boundary is that the input contract has not yet been discharged for
concrete Newstein/FGL geometry.
-/
def r1_concrete_newstein_fgl_to_native_map_input_contract_boundary : String :=
  "NO_DISCHARGED_INPUT_CONTRACT_FOR_NATIVE_CONSTRUCTION_MAP"

end Frontier
end Chronos
