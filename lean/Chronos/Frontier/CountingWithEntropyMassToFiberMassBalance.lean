import Chronos.Frontier.UniversalFiberEntropyGapFromCountingAndMass

namespace Chronos
namespace Frontier
namespace CountingWithEntropyMassToFiberMassBalance

open Chronos.Frontier.FiberLargeFromNonPropCore
open Chronos.Frontier.CountingFiberSeparationFromFiberLarge
open Chronos.Frontier.FiberMassBalanceFromNonPropInvariant
open Chronos.Frontier.UniversalFiberEntropyGapFromCountingAndMass

def CountingFiberSeparationWithEntropyMassFromNonProp
    (I : NonPropFinalCarrierInvariant) : Prop :=
  ∀ c : CarrierData,
    ∃ W : CountingFiberSeparationWitness,
      W.carrier = c ∧
      W.fiber.rankMass = I.rank c ∧
      W.fiber.fiberSize = I.fiberSize c ∧
      W.fiber.entropyMass = I.entropyMass c

theorem countingFiberSeparation_from_counting_with_entropy_mass
    (I : NonPropFinalCarrierInvariant)
    (h : CountingFiberSeparationWithEntropyMassFromNonProp I) :
    CountingFiberSeparationFromNonProp I := by
  intro c
  rcases h c with ⟨W, hcarrier, hrank, hfiber, _hentropy⟩
  exact ⟨W, hcarrier, hrank, hfiber⟩

theorem fiberMassBalance_from_counting_with_entropy_mass
    (I : NonPropFinalCarrierInvariant)
    (h : CountingFiberSeparationWithEntropyMassFromNonProp I) :
    FiberMassBalanceFromNonProp I := by
  intro c
  rcases h c with ⟨W, _hcarrier, hrank, _hfiber, hentropy⟩
  refine ⟨
    {
      carrier := c,
      rankMass := I.rank c,
      entropyMass := I.entropyMass c,
      positive_rank := ?_,
      rank_bounded_by_entropy := ?_
    },
    ?_
  ⟩
  · simpa [hrank] using W.positive_rank
  · simpa [hrank, hentropy] using W.rank_bounded_by_entropy
  · exact ⟨rfl, rfl, rfl⟩

theorem universalFiberEntropyGap_from_counting_with_entropy_mass
    (I : NonPropFinalCarrierInvariant)
    (h : CountingFiberSeparationWithEntropyMassFromNonProp I) :
    UniversalFiberEntropyGapFromNonProp I := by
  exact
    universalFiberEntropyGap_from_counting_and_mass
      I
      (countingFiberSeparation_from_counting_with_entropy_mass I h)
      (fiberMassBalance_from_counting_with_entropy_mass I h)

def FrontierStatus : String :=
  "COUNTING_WITH_ENTROPY_MASS_TO_FIBER_MASS_BALANCE_CLOSED"

def Boundary : String :=
  "Conditional enriched-counting bridge only; does not prove FiberMassBalance from ordinary CountingFiberSeparationFromNonProp alone; no unrestricted UniversalFiberEntropyGap, Chronos-RR, H4.1/FGL, P vs NP, or Clay closure"

end CountingWithEntropyMassToFiberMassBalance
end Frontier
end Chronos
