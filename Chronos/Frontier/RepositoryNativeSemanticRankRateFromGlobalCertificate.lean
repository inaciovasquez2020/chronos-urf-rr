import Chronos.Frontier.RepositoryNativeSemanticRankRateExhaustiveness

/-!
# RepositoryNativeSemanticRankRateExhaustiveness from a global certificate

A single global repository-native semantic rank-rate certificate is sufficient
to prove repository-native semantic rank-rate exhaustiveness, because
`RepositoryNativeSemanticRankRateDomain c` is independent of `c`.

Boundary:
- no global certificate is constructed here
- no proof of `native_semantic_rank_rate_certificate_exists`
- no unconditional `RepositoryNativeSemanticRankRateExhaustiveness`
- no unconditional `SemanticRankRateCertificate`
- no `SemanticRankRateToFiberEntropySoundness`
- no `UniversalFiberEntropyGap`
- no Chronos-RR closure
- no H4.1/FGL closure
- no P vs NP closure
- no Clay-problem closure
-/

theorem RepositoryNativeSemanticRankRateExhaustiveness_from_global_certificate
    (h : ∃ n : Nat, SemanticRankRateCertificate ChronosNativeCarrierFamily n) :
    RepositoryNativeSemanticRankRateExhaustiveness := by
  intro c hc
  exact h
