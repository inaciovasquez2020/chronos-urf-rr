import Chronos.Frontier.NonPropRankEntropyWitnessFrontier

namespace Chronos
namespace Frontier
namespace RankEntropyWitnessTwoObligationReduction

open Chronos.Frontier.FiberLargeExists
open Chronos.Frontier.NonPropRankEntropyWitnessFrontier

def LiveRankEntropyWitnessSelector : Prop :=
  ∀ c : ChronosCarrierData,
    FinalCarrierDomain c →
    ∃ F : Finset RankEntropyWitness,
      NonPropWitnessSet c F

def RankEntropyWitnessBridgeLaw : Prop :=
  ∀ c : ChronosCarrierData,
  ∀ F : Finset RankEntropyWitness,
    FinalCarrierDomain c →
    NonPropWitnessSet c F →
    RankRateGap c →
    FiberEntropyGap c

theorem nonPropRankEntropyWitnessFrontier_from_selector_and_bridge
    (hselector : LiveRankEntropyWitnessSelector)
    (hbridge : RankEntropyWitnessBridgeLaw) :
    NonPropRankEntropyWitnessFrontier := by
  intro c hc
  rcases hselector c hc with ⟨F, hF⟩
  refine ⟨F, hF, ?_⟩
  intro _hF_again hrank
  exact hbridge c F hc hF hrank

theorem semanticRankRateToFiberEntropySoundness_from_selector_and_bridge
    (hselector : LiveRankEntropyWitnessSelector)
    (hbridge : RankEntropyWitnessBridgeLaw) :
    SemanticRankRateToFiberEntropySoundness := by
  exact
    bridge_soundness_from_nonPropRankEntropyWitness
      (nonPropRankEntropyWitnessFrontier_from_selector_and_bridge hselector hbridge)

def FrontierStatus : String :=
  "FRONTIER_OPEN / TWO_OBLIGATION_REDUCTION_ONLY"

def TheoremLevelClosure : Bool :=
  false

end RankEntropyWitnessTwoObligationReduction
end Frontier
end Chronos
