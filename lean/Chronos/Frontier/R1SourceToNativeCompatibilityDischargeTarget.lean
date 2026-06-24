import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract
import Chronos.Frontier.FourBridgesRegistryIntegration

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
Invariant shape for the future source-to-native compatibility evidence.

This names the compatibility proposition that a future proof must discharge,
without supplying evidence for that proposition.
-/
structure R1SourceToNativeCompatibilityInvariantShape (D : R1SemanticData) : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  sourceToNativeCompatibilityInvariant : Prop

/--
The proposition carried by a source-to-native compatibility invariant shape.
This is only the target proposition; it is not evidence for the target.
-/
def r1_source_to_native_compatibility_invariant_shape_target
    (x : R1SourceToNativeCompatibilityInvariantShape D) : Prop :=
  x.sourceToNativeCompatibilityInvariant


/--
A source-to-native compatibility discharge target determines the corresponding
invariant-shape target proposition.

This is only a proposition-level bridge; it does not supply evidence for source
compatibility.
-/
def r1_source_to_native_compatibility_discharge_target_invariant_shape
    (D : R1SemanticData)
    (x : R1SourceToNativeCompatibilityDischargeTarget) :
    R1SourceToNativeCompatibilityInvariantShape D where
  source := x.source
  sourceToNativeCompatibilityInvariant := x.r1SourceToNativeCompatibility

/--
The invariant-shape target proposition extracted from a discharge target is
definitionally the discharge-target proposition.
-/
theorem r1_source_to_native_compatibility_discharge_target_invariant_shape_target_eq
    (D : R1SemanticData)
    (x : R1SourceToNativeCompatibilityDischargeTarget) :
    r1_source_to_native_compatibility_invariant_shape_target
      (r1_source_to_native_compatibility_discharge_target_invariant_shape D x) =
      x.r1SourceToNativeCompatibility := by
  rfl


/--
Evidence shape for the future source-to-native compatibility proof.

This is conditional data only: it packages an invariant shape together with an
inhabitant of its target proposition. It does not construct such an inhabitant.
-/
structure R1SourceToNativeCompatibilityEvidenceShape (D : R1SemanticData) : Type where
  invariant : R1SourceToNativeCompatibilityInvariantShape D
  compatibilityEvidence :
    r1_source_to_native_compatibility_invariant_shape_target invariant

/--
A compatibility evidence shape conditionally supplies the corresponding
source-to-native compatibility discharge target.
-/
def r1_source_to_native_compatibility_discharge_target_from_evidence_shape
    (x : R1SourceToNativeCompatibilityEvidenceShape D) :
    R1SourceToNativeCompatibilityDischargeTarget where
  source := x.invariant.source
  r1SourceToNativeCompatibility :=
    r1_source_to_native_compatibility_invariant_shape_target x.invariant
  sourceToNativeCompatibilityEvidence := x.compatibilityEvidence

/--
The discharge target obtained from an evidence shape has exactly the evidence
shape's invariant target proposition.
-/
theorem r1_source_to_native_compatibility_from_evidence_shape_target_eq
    (x : R1SourceToNativeCompatibilityEvidenceShape D) :
    (r1_source_to_native_compatibility_discharge_target_from_evidence_shape x).r1SourceToNativeCompatibility =
      r1_source_to_native_compatibility_invariant_shape_target x.invariant := by
  rfl

/--
An external Four Bridges source conditionally supplies a source-to-native
compatibility discharge target for the concrete Newstein/FGL source object by
using the repository-native R1/R2/R3 instance target supplied by the bridge
package.

This does not install an active bridge registry instance and does not prove an
unconditional native source-to-native compatibility theorem.
-/
def r1_source_to_native_compatibility_discharge_target_from_4bS
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (bridges : FourBridgesSource) :
    R1SourceToNativeCompatibilityDischargeTarget where
  source := x
  r1SourceToNativeCompatibility :=
    RepositoryNativeR1R2R3InstanceTarget
  sourceToNativeCompatibilityEvidence :=
    RepositoryNativeR1R2R3InstanceTarget_from_4bS bridges

theorem r1_source_to_native_compatibility_discharge_target_from_4bS_target_eq
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (bridges : FourBridgesSource) :
    (r1_source_to_native_compatibility_discharge_target_from_4bS x bridges).r1SourceToNativeCompatibility =
      RepositoryNativeR1R2R3InstanceTarget := by
  rfl

/--
The active boundary is that source-to-native compatibility has not yet been
discharged for the concrete Newstein/FGL source object.
-/
def r1_source_to_native_compatibility_discharge_target_boundary : String :=
  "NO_DISCHARGED_R1_SOURCE_TO_NATIVE_COMPATIBILITY_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT"

end Frontier
end Chronos
