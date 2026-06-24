import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract
import Chronos.Frontier.R1LongChordExclusionDischargeTarget
import Chronos.Frontier.R1DiameterSeparationFillingObstructionDischargeTarget
import Chronos.Frontier.R1UniformLocalTypeCapacityDischargeTarget
import Chronos.Frontier.R1SourceToNativeCompatibilityDischargeTarget
import Chronos.Frontier.FourBridgesRegistryIntegration

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

/--
An external Four Bridges source conditionally supplies aligned discharge targets
for the full R1 native-map input contract.

This packages the already-native concrete long-chord discharge target with the
R2, R3, and source-to-native compatibility targets supplied conditionally from
the external Four Bridges source.  It does not install an active bridge registry
instance and does not prove unconditional native R2/R3/source-compatibility
closure.
-/
def r1_concrete_newstein_fgl_to_native_map_aligned_discharge_targets_from_4bS
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (bridges : FourBridgesSource) :
    R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets
      R1ConcreteNativeSafeSemanticData where
  longChord := r1_concrete_newstein_fgl_source_long_chord_discharge_target x
  diameter :=
    r1_diameter_separation_filling_obstruction_discharge_target_from_4bS
      x bridges
  uniform :=
    r1_uniform_local_type_capacity_discharge_target_from_4bS
      x bridges
  compatibility :=
    r1_source_to_native_compatibility_discharge_target_from_4bS
      x bridges
  diameterSourceMatchesLongChord := rfl
  uniformSourceMatchesLongChord := rfl
  compatibilitySourceMatchesLongChord := rfl

/--
A Four Bridges source conditionally supplies the full R1 native-map input
contract for the concrete Newstein/FGL source object.

This remains conditional on `FourBridgesSource`.
-/
def r1_concrete_newstein_fgl_to_native_map_input_contract_from_4bS
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (bridges : FourBridgesSource) :
    R1ConcreteNewsteinFGLToNativeMapInputContract
      R1ConcreteNativeSafeSemanticData :=
  r1_concrete_newstein_fgl_to_native_map_input_contract_from_aligned_discharge_targets
    (r1_concrete_newstein_fgl_to_native_map_aligned_discharge_targets_from_4bS
      x bridges)

theorem r1_concrete_newstein_fgl_to_native_map_input_contract_from_4bS_diameter_eq
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (bridges : FourBridgesSource) :
    (r1_concrete_newstein_fgl_to_native_map_input_contract_from_4bS x bridges).r1DiameterSeparationFillingObstruction =
      DiameterSeparationFillingObstructionProofTarget := by
  rfl

theorem r1_concrete_newstein_fgl_to_native_map_input_contract_from_4bS_uniform_eq
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (bridges : FourBridgesSource) :
    (r1_concrete_newstein_fgl_to_native_map_input_contract_from_4bS x bridges).r1UniformLocalTypeCapacity =
      UniformLocalTypeCapacityProofTarget := by
  rfl

theorem r1_concrete_newstein_fgl_to_native_map_input_contract_from_4bS_compatibility_eq
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (bridges : FourBridgesSource) :
    (r1_concrete_newstein_fgl_to_native_map_input_contract_from_4bS x bridges).r1SourceToNativeCompatibility =
      RepositoryNativeR1R2R3InstanceTarget := by
  rfl

/--
If an active URF-11 bridge registry instance exists, its payload supplies the
same aligned discharge-target package.

This does not declare such an instance.
-/
def r1_concrete_newstein_fgl_to_native_map_aligned_discharge_targets_from_active_registry
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    [registry : URF11BridgeRegistry] :
    R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets
      R1ConcreteNativeSafeSemanticData :=
  r1_concrete_newstein_fgl_to_native_map_aligned_discharge_targets_from_4bS
    x registry.payload

/--
If an active URF-11 bridge registry instance exists, its payload conditionally
supplies the full R1 native-map input contract.

This does not declare such an instance.
-/
def r1_concrete_newstein_fgl_to_native_map_input_contract_from_active_registry
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    [registry : URF11BridgeRegistry] :
    R1ConcreteNewsteinFGLToNativeMapInputContract
      R1ConcreteNativeSafeSemanticData :=
  r1_concrete_newstein_fgl_to_native_map_input_contract_from_4bS
    x registry.payload

end Frontier
end Chronos
