namespace Chronos
namespace Frontier

structure DepthBridgeInstance where
  Carrier : Type
  Lambda : Type
  ObsDim : Lambda → Nat
  TranscriptDim : Carrier → Lambda → Nat

structure CarrierAdmissible
    (I : DepthBridgeInstance) where
  carrier : I.Carrier

structure FiberEntropyGap
    (I : DepthBridgeInstance)
    (A : CarrierAdmissible I) where
  alpha_num : Nat
  alpha_den : Nat
  alpha_pos : alpha_num > 0
  alpha_le_den : alpha_num ≤ alpha_den
  eventually_gap :
    ∀ lam : I.Lambda,
      alpha_den * I.TranscriptDim A.carrier lam
        ≤ (alpha_den - alpha_num) * I.ObsDim lam

structure RankImageBound
    (I : DepthBridgeInstance)
    (A : CarrierAdmissible I) where
  alpha_num : Nat
  alpha_den : Nat
  alpha_pos : alpha_num > 0
  eventually_rank_bound :
    ∀ lam : I.Lambda,
      alpha_den * I.TranscriptDim A.carrier lam
        ≤ (alpha_den - alpha_num) * I.ObsDim lam

def depthBridgeFiberGap_to_rankImageBound
    (I : DepthBridgeInstance)
    (A : CarrierAdmissible I)
    (G : FiberEntropyGap I A) :
    RankImageBound I A :=
{
  alpha_num := G.alpha_num
  alpha_den := G.alpha_den
  alpha_pos := G.alpha_pos
  eventually_rank_bound := G.eventually_gap
}

end Frontier
end Chronos
