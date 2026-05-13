import Chronos.Frontier.FiberLargeExistsCertifiedSurface

namespace Chronos
namespace Frontier
namespace NonPropRankEntropyWitnessFrontier

open Chronos.Frontier.FiberLargeExists

structure RankEntropyWitness where
  fiber : FiberWitness
  rankMass : Nat
  entropyMass : Nat
deriving DecidableEq, Repr

def RankEntropyWitnessLive (w : RankEntropyWitness) : Prop :=
  0 < w.rankMass ∧ w.rankMass ≤ w.entropyMass

def NonPropWitnessSet
    (c : ChronosCarrierData)
    (F : Finset RankEntropyWitness) : Prop :=
  F.Nonempty ∧
  ∀ w : RankEntropyWitness,
    w ∈ F →
      w.fiber.carrierId = c.arity ∧
      RankEntropyWitnessLive w

def NonPropRankEntropyWitnessFrontier : Prop :=
  ∀ c : ChronosCarrierData,
    FinalCarrierDomain c →
    ∃ F : Finset RankEntropyWitness,
      NonPropWitnessSet c F ∧
      (NonPropWitnessSet c F → RankRateGap c → FiberEntropyGap c)

def BridgeSoundnessFromNonPropRankEntropyWitness : Prop :=
  NonPropRankEntropyWitnessFrontier →
    SemanticRankRateToFiberEntropySoundness

theorem bridge_soundness_from_nonPropRankEntropyWitness :
    BridgeSoundnessFromNonPropRankEntropyWitness := by
  intro h
  intro c hc hrank
  rcases h c hc with ⟨F, hF, hbridge⟩
  exact hbridge hF hrank

def FrontierStatus : String :=
  "FRONTIER_OPEN / WEAKEST_MISSING_NONPROP_WITNESS_ONLY"

def TheoremLevelClosure : Bool :=
  false

end NonPropRankEntropyWitnessFrontier
end Frontier
end Chronos
