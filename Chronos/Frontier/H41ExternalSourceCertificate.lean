import Chronos.Frontier.H41CertifiedFamily

namespace Chronos.Frontier

universe u

abbrev H41LocalIndistinguishabilityStatement : Prop :=
  ∀ k Δ r n : Nat,
    ∀ τ : Transcript.{u},
      TranscriptOf.{u,u,u} (SearchFn.{u,u} k Δ r n) τ →
      RevealedBits.{u} τ * h41_c_den k Δ r < n →
      ∃ x y : AdmissibleCertificatePlacements.{u,u} (Fn.{u} k Δ r n),
        support.{u} (mu_n.{u,u} k Δ r n) x ∧
        support.{u} (mu_n.{u,u} k Δ r n) y ∧
        LocallyIndistinguishableUpToTranscript.{u,u} τ x y ∧
        SearchOutput.{u,u,u} (SearchFn.{u,u} k Δ r n) x ≠
          SearchOutput.{u,u,u} (SearchFn.{u,u} k Δ r n) y

structure ExternalH41SourceCertificate : Type (u + 1) where
  source_id : String
  source_title : String
  localIndistinguishability : H41LocalIndistinguishabilityStatement.{u}

def CONDITIONAL_H41_PAYLOAD_REQUIRED : Prop :=
  Nonempty (ExternalH41SourceCertificate.{u})

theorem H41_LocalIndistinguishability_payload_required
    (cert : ExternalH41SourceCertificate.{u}) :
    H41LocalIndistinguishabilityStatement.{u} :=
  cert.localIndistinguishability

theorem H41_LocalIndistinguishability_restricted
    (h : H41LocalIndistinguishabilityStatement.{u}) :
    H41LocalIndistinguishabilityStatement.{u} :=
  h

end Chronos.Frontier
