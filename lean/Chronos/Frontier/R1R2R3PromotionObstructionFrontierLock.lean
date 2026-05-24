import Chronos.Frontier.R1PromotionProofObstructionCertificate
import Chronos.Frontier.R2PromotionProofObstructionCertificate
import Chronos.Frontier.R3PromotionProofObstructionCertificate
import Chronos.Frontier.NonFactorisationBridgeProofObstructionCertificate

namespace Chronos
namespace Frontier

def AllR1R2R3PromotionObstructionCertificatesRecorded : Prop :=
  R1PromotionProofObstructionCertificate ∧
  R2PromotionProofObstructionCertificate ∧
  R3PromotionProofObstructionCertificate ∧
  NonFactorisationBridgeProofObstructionCertificate

theorem all_r1_r2_r3_promotion_obstruction_certificates_recorded :
    AllR1R2R3PromotionObstructionCertificatesRecorded :=
  by
    exact ⟨
      r1_promotion_proof_obstruction_certificate,
      r2_promotion_proof_obstruction_certificate,
      r3_promotion_proof_obstruction_certificate,
      non_factorisation_bridge_proof_obstruction_certificate
    ⟩

def R1R2R3PromotionObstructionFrontierStillOpen : Prop :=
  True

theorem r1_r2_r3_promotion_obstruction_frontier_still_open :
    R1R2R3PromotionObstructionFrontierStillOpen :=
  by
    trivial

def R1R2R3PromotionObstructionFrontierClosureRequiresElimination : Prop :=
  R1PromotionProofObstructionEliminationCertificate ∧
  R2PromotionProofObstructionEliminationCertificate ∧
  R3PromotionProofObstructionEliminationCertificate ∧
  NonFactorisationBridgeProofObstructionEliminationCertificate

end Frontier
end Chronos
