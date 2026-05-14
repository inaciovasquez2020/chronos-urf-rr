import Chronos.Frontier.FiberMassBalanceFromNonPropInvariant

namespace Chronos
namespace Frontier
namespace UniversalFiberEntropyGapFromCountingAndMass

open Chronos.Frontier.FiberLargeFromNonPropCore
open Chronos.Frontier.CountingFiberSeparationFromFiberLarge
open Chronos.Frontier.FiberMassBalanceFromNonPropInvariant

structure UniversalFiberEntropyGapWitness where
  carrier : CarrierData
  counting : CountingFiberSeparationWitness
  massBalance : FiberMassBalanceWitness
  counting_carrier : counting.carrier = carrier
  mass_balance_carrier : massBalance.carrier = carrier
  rank_agrees : counting.fiber.rankMass = massBalance.rankMass
  entropy_controls_rank : (counting.fiber.rankMass : Rat) ≤ massBalance.entropyMass
deriving Repr

def UniversalFiberEntropyGapFromNonProp
    (I : NonPropFinalCarrierInvariant) : Prop :=
  ∀ c : CarrierData,
    ∃ W : UniversalFiberEntropyGapWitness,
      W.carrier = c ∧
      W.counting.fiber.rankMass = I.rank c ∧
      W.massBalance.entropyMass = I.entropyMass c

theorem universalFiberEntropyGap_from_counting_and_mass
    (I : NonPropFinalCarrierInvariant)
    (hcount : CountingFiberSeparationFromNonProp I)
    (hmass : FiberMassBalanceFromNonProp I) :
    UniversalFiberEntropyGapFromNonProp I := by
  intro c
  rcases hcount c with ⟨Wc, hWc_carrier, hWc_rank, _hWc_fiber⟩
  rcases hmass c with ⟨Wm, hWm_carrier, hWm_rank, hWm_entropy⟩
  refine ⟨
    {
      carrier := c,
      counting := Wc,
      massBalance := Wm,
      counting_carrier := hWc_carrier,
      mass_balance_carrier := hWm_carrier,
      rank_agrees := hWc_rank.trans hWm_rank.symm,
      entropy_controls_rank := ?_
    },
    ?_
  ⟩
  · simpa [hWc_rank, hWm_rank] using Wm.rank_bounded_by_entropy
  · exact ⟨rfl, hWc_rank, hWm_entropy⟩

theorem universalFiberEntropyGap_from_nonprop_invariant
    (I : NonPropFinalCarrierInvariant) :
    UniversalFiberEntropyGapFromNonProp I := by
  exact
    universalFiberEntropyGap_from_counting_and_mass
      I
      (countingFiberSeparation_from_nonprop_invariant I)
      (fiberMassBalance_from_nonprop_invariant I)

def FrontierStatus : String :=
  "LAKE_NATIVE_UNIVERSAL_FIBER_ENTROPY_GAP_FROM_COUNTING_AND_MASS_CLOSED"

def Boundary : String :=
  "Lake-native UniversalFiberEntropyGap assembly only; no Chronos-RR, H4.1/FGL, P vs NP, or Clay closure"

end UniversalFiberEntropyGapFromCountingAndMass
end Frontier
end Chronos
