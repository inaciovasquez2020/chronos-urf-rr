import Chronos.Frontier.R1NativeCounterexampleCoherentRestriction
import Chronos.Frontier.R1R2R3AxiomBoundaryClosure

namespace Chronos
namespace Frontier

/--
R1 finished native theorem.

Unrestricted native R1 is false; the finished native R1 theorem is the
coherent restricted theorem.
-/
def R1FinishedTheorem : Prop :=
  R1CoherentLongChordExclusionProofTarget

theorem R1FinishedTheorem_proved :
    R1FinishedTheorem :=
  R1CoherentLongChordExclusionProofTarget_proved

/--
R2 finished native theorem.

The separation floor survives diameter/filling compatibility by monotonicity.
-/
def R2FinishedTheorem : Prop :=
  ∀ x : DiameterFillingNativeObject,
    DiameterFillingCompatibility x →
      x.separationFloor <= x.targetDiameter + x.fillingCost

theorem R2FinishedTheorem_proved :
    R2FinishedTheorem :=
  monotone_separation_lower_bound

/--
R3 finished native theorem.

Any native local-type object below the explicit capacity bound lies within
the explicit capacity.
-/
def R3FinishedTheorem : Prop :=
  ∀ x : LocalTypeCapacityNativeObject,
    x.localTypeCount <= ExplicitLocalTypeCapacityC →
      WithinExplicitLocalTypeCapacity x

theorem R3FinishedTheorem_proved :
    R3FinishedTheorem :=
  local_type_capacity_bound_certificate

/--
Finite R2 and R3 packets remain certified inputs, but they are not the
semantic source for the opaque targets.
-/
theorem R2FiniteCertifiedInputStillAvailable :
    R2FiniteDiameterSeparationFillingDataCertified :=
  r2_finite_diameter_separation_filling_data_certified

theorem R3FiniteCertifiedInputStillAvailable :
    R3FiniteUniformLocalTypeCapacityDataCertified :=
  r3_finite_uniform_local_type_capacity_data_certified

/--
4bS: Four Bridges Source.

This is the external certification package. It supplies exactly the four
semantic bridges needed to pass from the finished native kernels to the
the opaque repository targets and then to NON_FACTORISATION.
-/
structure FourBridgesSource : Prop where
  r1 : R1FinishedTheorem → LongChordExclusionProofTarget
  r2 : R2FinishedTheorem → DiameterSeparationFillingObstructionProofTarget
  r3 : R3FinishedTheorem → UniformLocalTypeCapacityProofTarget
  r4 : RepositoryNativeR1R2R3InstanceTarget → NonFactorisationProofTarget

def FourBridgesSourceStatus : String :=
  "4bS_SUPPLIED_BRIDGE_PACKAGE"

def FourBridgesRegistryPolicyStatus : String :=
  "EXTERNAL_4bS_CERTIFICATION_ONLY"

def FourBridgesRegistryRejectedPaths : List String :=
  [
    "native active registry instance",
    "global bridge declaration",
    "macro or meta-program injection",
    "unconditional opaque-target closure without 4bS"
  ]

theorem R1_from_4bS
    (bridges : FourBridgesSource) :
    LongChordExclusionProofTarget :=
  bridges.r1 R1FinishedTheorem_proved

theorem R2_from_4bS
    (bridges : FourBridgesSource) :
    DiameterSeparationFillingObstructionProofTarget :=
  bridges.r2 R2FinishedTheorem_proved

theorem R3_from_4bS
    (bridges : FourBridgesSource) :
    UniformLocalTypeCapacityProofTarget :=
  bridges.r3 R3FinishedTheorem_proved

theorem RepositoryNativeR1R2R3InstanceTarget_from_4bS
    (bridges : FourBridgesSource) :
    RepositoryNativeR1R2R3InstanceTarget :=
  And.intro
    (R1_from_4bS bridges)
    (And.intro
      (R2_from_4bS bridges)
      (R3_from_4bS bridges))

theorem R4_from_4bS
    (bridges : FourBridgesSource) :
    NonFactorisationProofTarget :=
  bridges.r4 (RepositoryNativeR1R2R3InstanceTarget_from_4bS bridges)

theorem CompleteOpaqueSystem_conditional_on_4bS
    (bridges : FourBridgesSource) :
    LongChordExclusionProofTarget ∧
    DiameterSeparationFillingObstructionProofTarget ∧
    UniformLocalTypeCapacityProofTarget ∧
    NonFactorisationProofTarget := by
  exact ⟨
    R1_from_4bS bridges,
    R2_from_4bS bridges,
    R3_from_4bS bridges,
    R4_from_4bS bridges
  ⟩

/--
URF-11 bridge registry typeclass.

No active instance is declared in this file. External 4bS certification must
supply an instance outside the native kernel.
-/
class URF11BridgeRegistry where
  payload : FourBridgesSource
  status_check : FourBridgesSourceStatus = "4bS_SUPPLIED_BRIDGE_PACKAGE" := by
    rfl

theorem R1_registered_extraction [registry : URF11BridgeRegistry] :
    LongChordExclusionProofTarget :=
  R1_from_4bS registry.payload

theorem R2_registered_extraction [registry : URF11BridgeRegistry] :
    DiameterSeparationFillingObstructionProofTarget :=
  R2_from_4bS registry.payload

theorem R3_registered_extraction [registry : URF11BridgeRegistry] :
    UniformLocalTypeCapacityProofTarget :=
  R3_from_4bS registry.payload

theorem R4_registered_extraction [registry : URF11BridgeRegistry] :
    NonFactorisationProofTarget :=
  R4_from_4bS registry.payload

theorem CompleteOpaqueSystem_registered [registry : URF11BridgeRegistry] :
    LongChordExclusionProofTarget ∧
    DiameterSeparationFillingObstructionProofTarget ∧
    UniformLocalTypeCapacityProofTarget ∧
    NonFactorisationProofTarget :=
  CompleteOpaqueSystem_conditional_on_4bS registry.payload

def FourBridgesRegistryIntegrationStatus : String :=
  "FOUR_BRIDGES_REGISTRY_INTEGRATION_CONDITIONAL_EXTERNAL_ONLY"

def FourBridgesRegistryIntegrationBoundary : String :=
  "Does not provide an active URF11BridgeRegistry instance; does not prove unconditional opaque R1, R2, R3, R4, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem."

end Frontier
end Chronos
