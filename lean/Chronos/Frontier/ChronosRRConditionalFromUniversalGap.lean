import Chronos.Frontier.UniversalFiberEntropyGapFromCountingAndMass

namespace Chronos
namespace Frontier
namespace ChronosRRConditionalFromUniversalGap

open Chronos.Frontier.FiberLargeFromNonPropCore
open Chronos.Frontier.UniversalFiberEntropyGapFromCountingAndMass

structure ChronosRRConditionalWitness where
  carrier : CarrierData
  universalGap : UniversalFiberEntropyGapWitness
  universal_gap_carrier : universalGap.carrier = carrier
  rank_mass_present : 0 < universalGap.massBalance.rankMass
  entropy_controls_rank :
    (universalGap.counting.fiber.rankMass : Rat) ≤ universalGap.massBalance.entropyMass
deriving Repr

def ChronosRRConditionalFromNonProp
    (I : NonPropFinalCarrierInvariant) : Prop :=
  ∀ c : CarrierData,
    ∃ W : ChronosRRConditionalWitness,
      W.carrier = c ∧
      W.universalGap.counting.fiber.rankMass = I.rank c ∧
      W.universalGap.massBalance.entropyMass = I.entropyMass c

theorem chronosRRConditional_from_universalFiberEntropyGap
    (I : NonPropFinalCarrierInvariant)
    (hgap : UniversalFiberEntropyGapFromNonProp I) :
    ChronosRRConditionalFromNonProp I := by
  intro c
  rcases hgap c with ⟨W, hW_carrier, hW_rank, hW_entropy⟩
  refine ⟨
    {
      carrier := c,
      universalGap := W,
      universal_gap_carrier := hW_carrier,
      rank_mass_present := ?_,
      entropy_controls_rank := W.entropy_controls_rank
    },
    ?_
  ⟩
  · rw [← W.rank_agrees]
    exact W.counting.positive_rank
  · exact ⟨rfl, hW_rank, hW_entropy⟩

theorem chronosRRConditional_from_nonprop_invariant
    (I : NonPropFinalCarrierInvariant) :
    ChronosRRConditionalFromNonProp I := by
  exact
    chronosRRConditional_from_universalFiberEntropyGap
      I
      (universalFiberEntropyGap_from_nonprop_invariant I)

def FrontierStatus : String :=
  "LAKE_NATIVE_CHRONOS_RR_CONDITIONAL_FROM_UNIVERSAL_GAP_CLOSED"

def Boundary : String :=
  "Lake-native Chronos-RR conditional promotion only; no unrestricted Chronos-RR, H4.1/FGL, P vs NP, or Clay closure"

end ChronosRRConditionalFromUniversalGap
end Frontier
end Chronos
