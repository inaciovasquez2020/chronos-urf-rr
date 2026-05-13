import Chronos.Frontier.RankEntropyWitnessTwoObligationReduction

namespace Chronos
namespace Frontier
namespace LiveRankEntropyWitnessSelectorSurface

open Chronos.Frontier.FiberLargeExists
open Chronos.Frontier.NonPropRankEntropyWitnessFrontier
open Chronos.Frontier.RankEntropyWitnessTwoObligationReduction

def canonicalRankEntropyWitness (c : ChronosCarrierData) : RankEntropyWitness :=
  {
    fiber := { carrierId := c.arity, fiberId := 0 },
    rankMass := 1,
    entropyMass := 1
  }

def canonicalRankEntropyWitnessSet (c : ChronosCarrierData) : Finset RankEntropyWitness :=
  { canonicalRankEntropyWitness c }

theorem canonicalRankEntropyWitnessSet_nonempty
    (c : ChronosCarrierData) :
    (canonicalRankEntropyWitnessSet c).Nonempty := by
  refine ⟨canonicalRankEntropyWitness c, ?_⟩
  simp [canonicalRankEntropyWitnessSet]

theorem canonicalRankEntropyWitness_live
    (c : ChronosCarrierData) :
    RankEntropyWitnessLive (canonicalRankEntropyWitness c) := by
  simp [RankEntropyWitnessLive, canonicalRankEntropyWitness]

theorem canonicalRankEntropyWitnessSet_is_nonPropWitnessSet
    (c : ChronosCarrierData) :
    NonPropWitnessSet c (canonicalRankEntropyWitnessSet c) := by
  constructor
  · exact canonicalRankEntropyWitnessSet_nonempty c
  · intro w hw
    rw [canonicalRankEntropyWitnessSet] at hw
    rw [Finset.mem_singleton] at hw
    subst w
    exact ⟨rfl, canonicalRankEntropyWitness_live c⟩

theorem liveRankEntropyWitnessSelector_surface :
    LiveRankEntropyWitnessSelector := by
  intro c _hc
  exact ⟨canonicalRankEntropyWitnessSet c, canonicalRankEntropyWitnessSet_is_nonPropWitnessSet c⟩

def FrontierStatus : String :=
  "SELECTOR_SURFACE_CLOSED_ONLY"

def RemainingObligation : String :=
  "RankEntropyWitnessBridgeLaw"

def TheoremLevelClosure : Bool :=
  false

end LiveRankEntropyWitnessSelectorSurface
end Frontier
end Chronos
