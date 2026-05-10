namespace Chronos
namespace Frontier
namespace CarrierSupportSignatureInvariant

structure Carrier where
  id : String

structure SupportSignature where
  id : String

constant ChronosAdmissible : Carrier → Prop
constant HasSupportSignature : Carrier → SupportSignature → Prop
constant RepositoryRealizesSignature : SupportSignature → Prop
constant RepositoryRegistersCarrier : Carrier → Prop

def status : String := "CONDITIONAL_CLASSIFICATION_INVARIANT"

def invariantName : String :=
  "CarrierSupportSignatureInvariant"

def invariantStatement : String :=
  "Every Chronos-admissible carrier has a finite support signature realized by the repository registry."

def preservedFrontier : String :=
  "CarrierRegistryExhaustiveness remains FRONTIER_OPEN unless the support-signature classification hypothesis is proved."

def boundaryCarrierRegistryExhaustiveness : String :=
  "NO_CARRIER_REGISTRY_EXHAUSTIVENESS_PROOF"

def boundaryUnrestrictedRegSNF : String :=
  "NO_UNRESTRICTED_REG_SNF_CLOSURE"

def boundaryUniversalFiberEntropyGap : String :=
  "NO_UNIVERSAL_FIBER_ENTROPY_GAP_PROOF"

def boundaryDepthBridge : String :=
  "NO_DEPTH_BRIDGE_EXTENSION_BEYOND_SELECTED_FINAL_CARRIER_DOMAIN"

def boundaryChronosRR : String :=
  "NO_CHRONOS_RR_CLOSURE"

def boundaryH41FGL : String :=
  "NO_H4_1_FGL_CLOSURE"

def boundaryPvsNP : String :=
  "NO_P_VS_NP_CLOSURE"

def boundaryClay : String :=
  "NO_CLAY_PROBLEM_CLOSURE"

def RegistryRealizationRegistersCarrier : Prop :=
  ∀ (C : Carrier) (S : SupportSignature),
    HasSupportSignature C S →
    RepositoryRealizesSignature S →
    RepositoryRegistersCarrier C

theorem conditional_carrier_registry_exhaustiveness_from_support_signature :
  RegistryRealizationRegistersCarrier →
  (∀ C : Carrier,
      ChronosAdmissible C →
        ∃ S : SupportSignature,
          HasSupportSignature C S ∧ RepositoryRealizesSignature S) →
  (∀ C : Carrier,
      ChronosAdmissible C →
        RepositoryRegistersCarrier C) := by
  intro hRealizes hClassifies C hC
  rcases hClassifies C hC with ⟨S, hSig, hReg⟩
  exact hRealizes C S hSig hReg

end CarrierSupportSignatureInvariant
end Frontier
end Chronos
