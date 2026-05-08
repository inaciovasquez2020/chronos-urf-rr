namespace Chronos
namespace Frontier

structure CertificateDepthBridgeInstance where
  Carrier : Type
  Lambda : Type
  ObsDim : Lambda → Nat
  TranscriptDim : Carrier → Lambda → Nat

structure CertificateCarrierAdmissible
    (I : CertificateDepthBridgeInstance) where
  carrier : I.Carrier

structure CertificateFiberEntropyGap
    (I : CertificateDepthBridgeInstance)
    (A : CertificateCarrierAdmissible I) where
  alpha_num : Nat
  alpha_den : Nat
  alpha_pos : alpha_num > 0
  alpha_le_den : alpha_num ≤ alpha_den
  certified_gap :
    ∀ lam : I.Lambda,
      alpha_den * I.TranscriptDim A.carrier lam
        ≤ (alpha_den - alpha_num) * I.ObsDim lam

structure CertificateRankImageBound
    (I : CertificateDepthBridgeInstance)
    (A : CertificateCarrierAdmissible I) where
  alpha_num : Nat
  alpha_den : Nat
  alpha_pos : alpha_num > 0
  certified_rank_bound :
    ∀ lam : I.Lambda,
      alpha_den * I.TranscriptDim A.carrier lam
        ≤ (alpha_den - alpha_num) * I.ObsDim lam

def certificateFiberEntropyGap_to_rankImageBound
    (I : CertificateDepthBridgeInstance)
    (A : CertificateCarrierAdmissible I)
    (Cert : CertificateFiberEntropyGap I A) :
    CertificateRankImageBound I A :=
{
  alpha_num := Cert.alpha_num
  alpha_den := Cert.alpha_den
  alpha_pos := Cert.alpha_pos
  certified_rank_bound := Cert.certified_gap
}

end Frontier
end Chronos
