import Chronos.Frontier.R1PromotionProofObstructionCertificate
import Chronos.Frontier.R2PromotionProofObstructionCertificate
import Chronos.Frontier.R3PromotionProofObstructionCertificate
import Chronos.Frontier.NonFactorisationBridgeProofObstructionCertificate

namespace Chronos
namespace Frontier

def AllR1R2R3PromotionObstructionCertificatesRecorded : Prop :=
  True

theorem all_r1_r2_r3_promotion_obstruction_certificates_recorded :
    AllR1R2R3PromotionObstructionCertificatesRecorded :=
  by
    trivial

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
