import Chronos.Frontier.FiberLargeFromNonPropCore

namespace Chronos
namespace Frontier
namespace CountingFiberSeparationFromFiberLarge

open Chronos.Frontier.FiberLargeFromNonPropCore

structure CountingFiberSeparationWitness where
  carrier : CarrierData
  fiber : FiberWitness
  carrier_matches : fiber.carrierId = carrier.arity
  positive_rank : 0 < fiber.rankMass
  rank_bounded_by_fiber : fiber.rankMass ≤ fiber.fiberSize
  rank_bounded_by_entropy : (fiber.rankMass : Rat) ≤ fiber.entropyMass
deriving Repr

def CountingFiberSeparationFromNonProp
    (I : NonPropFinalCarrierInvariant) : Prop :=
  ∀ c : CarrierData,
    ∃ W : CountingFiberSeparationWitness,
      W.carrier = c ∧
      W.fiber.rankMass = I.rank c ∧
      W.fiber.fiberSize = I.fiberSize c

theorem countingFiberSeparation_from_fiberLargeExists
    (I : NonPropFinalCarrierInvariant)
    (h : FiberLargeExistsFromNonProp I) :
    CountingFiberSeparationFromNonProp I := by
  intro c
  rcases h c with
    ⟨w, hcarrier, hrank, hfiber, hrank_pos, hrank_fiber, hrank_entropy⟩
  refine ⟨
    {
      carrier := c,
      fiber := w,
      carrier_matches := hcarrier,
      positive_rank := hrank_pos,
      rank_bounded_by_fiber := hrank_fiber,
      rank_bounded_by_entropy := hrank_entropy
    },
    ?_
  ⟩
  exact ⟨rfl, hrank, hfiber⟩

theorem countingFiberSeparation_from_nonprop_invariant
    (I : NonPropFinalCarrierInvariant) :
    CountingFiberSeparationFromNonProp I := by
  exact
    countingFiberSeparation_from_fiberLargeExists
      I
      (fiberLargeExists_from_nonprop_invariant I)

def FrontierStatus : String :=
  "LAKE_NATIVE_COUNTING_FIBER_SEPARATION_FROM_FIBER_LARGE_CLOSED"

def Boundary : String :=
  "Lake-native counting-separation theorem only; no FiberMassBalance, UniversalFiberEntropyGap, Chronos-RR, H4.1/FGL, P vs NP, or Clay closure"

end CountingFiberSeparationFromFiberLarge
end Frontier
end Chronos
