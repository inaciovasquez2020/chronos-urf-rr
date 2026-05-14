import Chronos.Frontier.CountingFiberSeparationFromFiberLarge

namespace Chronos
namespace Frontier
namespace FiberMassBalanceFromNonPropInvariant

open Chronos.Frontier.FiberLargeFromNonPropCore
open Chronos.Frontier.CountingFiberSeparationFromFiberLarge

structure FiberMassBalanceWitness where
  carrier : CarrierData
  rankMass : Nat
  entropyMass : Rat
  positive_rank : 0 < rankMass
  rank_bounded_by_entropy : (rankMass : Rat) ≤ entropyMass
deriving Repr

def FiberMassBalanceFromNonProp
    (I : NonPropFinalCarrierInvariant) : Prop :=
  ∀ c : CarrierData,
    ∃ W : FiberMassBalanceWitness,
      W.carrier = c ∧
      W.rankMass = I.rank c ∧
      W.entropyMass = I.entropyMass c

theorem fiberMassBalance_from_nonprop_invariant
    (I : NonPropFinalCarrierInvariant) :
    FiberMassBalanceFromNonProp I := by
  intro c
  refine ⟨
    {
      carrier := c,
      rankMass := I.rank c,
      entropyMass := I.entropyMass c,
      positive_rank := I.rank_positive c,
      rank_bounded_by_entropy := I.entropy_mass_lower c
    },
    ?_
  ⟩
  exact ⟨rfl, rfl, rfl⟩

theorem countingFiberSeparation_and_fiberMassBalance_from_nonprop_invariant
    (I : NonPropFinalCarrierInvariant) :
    CountingFiberSeparationFromNonProp I ∧ FiberMassBalanceFromNonProp I := by
  exact ⟨
    countingFiberSeparation_from_nonprop_invariant I,
    fiberMassBalance_from_nonprop_invariant I
  ⟩

def FrontierStatus : String :=
  "LAKE_NATIVE_FIBER_MASS_BALANCE_FROM_NONPROP_INVARIANT_CLOSED"

def Boundary : String :=
  "Lake-native fiber-mass-balance theorem only; no UniversalFiberEntropyGap, Chronos-RR, H4.1/FGL, P vs NP, or Clay closure"

end FiberMassBalanceFromNonPropInvariant
end Frontier
end Chronos
