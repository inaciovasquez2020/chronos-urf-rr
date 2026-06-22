import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract
import Chronos.Frontier.R1LongChordExclusionDischargeTarget
import Chronos.Frontier.R1DiameterSeparationFillingObstructionDischargeTarget
import Chronos.Frontier.R1UniformLocalTypeCapacityDischargeTarget
import Chronos.Frontier.R1SourceToNativeCompatibilityDischargeTarget

namespace Chronos
namespace Frontier

/--
Aligned discharge targets for the full R1 native-map input contract.

This is conditional data only: it assumes all four target objects, including the
still-missing evidence fields, and records that they refer to the same concrete
source object.
-/
structure R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets
    (D : R1SemanticData) : Type where
  longChord : R1LongChordExclusionDischargeTarget D
  diameter : R1DiameterSeparationFillingObstructionDischargeTarget
  uniform : R1UniformLocalTypeCapacityDischargeTarget
  compatibility : R1SourceToNativeCompatibilityDischargeTarget
  diameterSourceMatchesLongChord : diameter.source = longChord.source
  uniformSourceMatchesLongChord : uniform.source = longChord.source
  compatibilitySourceMatchesLongChord : compatibility.source = longChord.source

/--
Conditional constructor for the full R1 native-map input contract from aligned
discharge targets.

This does not prove any missing field. It only assembles the full contract after
the four evidence-bearing discharge targets have already been supplied.
-/
def r1_concrete_newstein_fgl_to_native_map_input_contract_from_aligned_discharge_targets
    (x : R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets D) :
    R1ConcreteNewsteinFGLToNativeMapInputContract D where
  source := x.longChord.source
  r1LongChordExclusion := x.longChord.r1LongChordExclusion
  r1DiameterSeparationFillingObstruction :=
    x.diameter.r1DiameterSeparationFillingObstruction
  r1UniformLocalTypeCapacity := x.uniform.r1UniformLocalTypeCapacity
  r1SourceToNativeCompatibility := x.compatibility.r1SourceToNativeCompatibility
  longChordExclusionEvidence := x.longChord.longChordExclusionEvidence
  diameterSeparationFillingObstructionEvidence :=
    x.diameter.diameterSeparationFillingObstructionEvidence
  uniformLocalTypeCapacityEvidence := x.uniform.uniformLocalTypeCapacityEvidence
  sourceToNativeCompatibilityEvidence :=
    x.compatibility.sourceToNativeCompatibilityEvidence

theorem r1_native_map_input_contract_from_aligned_targets_long_chord_eq
    (x : R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets D) :
    (r1_concrete_newstein_fgl_to_native_map_input_contract_from_aligned_discharge_targets x).r1LongChordExclusion =
      x.longChord.r1LongChordExclusion := by
  rfl

theorem r1_native_map_input_contract_from_aligned_targets_diameter_eq
    (x : R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets D) :
    (r1_concrete_newstein_fgl_to_native_map_input_contract_from_aligned_discharge_targets x).r1DiameterSeparationFillingObstruction =
      x.diameter.r1DiameterSeparationFillingObstruction := by
  rfl

theorem r1_native_map_input_contract_from_aligned_targets_uniform_eq
    (x : R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets D) :
    (r1_concrete_newstein_fgl_to_native_map_input_contract_from_aligned_discharge_targets x).r1UniformLocalTypeCapacity =
      x.uniform.r1UniformLocalTypeCapacity := by
  rfl

theorem r1_native_map_input_contract_from_aligned_targets_compatibility_eq
    (x : R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets D) :
    (r1_concrete_newstein_fgl_to_native_map_input_contract_from_aligned_discharge_targets x).r1SourceToNativeCompatibility =
      x.compatibility.r1SourceToNativeCompatibility := by
  rfl

end Frontier
end Chronos
