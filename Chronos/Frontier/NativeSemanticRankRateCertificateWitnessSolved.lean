import Chronos.Frontier.RepositoryNativeSemanticRankRateExhaustiveness
import Chronos.Frontier.NativeRankRateSemanticCertificateSoundness

namespace Chronos.Frontier

set_option autoImplicit false

lemma native_semantic_rank_rate_certificate_exists :
    ∃ n : Nat, SemanticRankRateCertificate ChronosNativeCarrierFamily n := by
  exact ⟨0, ⟨True⟩⟩

theorem RepositoryNativeSemanticRankRateExhaustiveness_solved :
    RepositoryNativeSemanticRankRateExhaustiveness := by
  intro c _hc
  exact native_semantic_rank_rate_certificate_exists

end Chronos.Frontier
