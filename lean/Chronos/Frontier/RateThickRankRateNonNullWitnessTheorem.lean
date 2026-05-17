import Chronos.Frontier.SimplexEntropyCoercivityAxiom

namespace Chronos
namespace Frontier
namespace RateThickRankRateNonNullWitnessTheorem

open SimplexEntropyCoercivityAxiom
open RateThickFiberCoercivityTheorem

noncomputable section

/-- Concrete rank-rate non-null witness on a rate-thick Chronos state. -/
def RateThickRankRateNonNullWitnessConcrete
    (S : ChronosThickState) : Prop :=
  ∀ p : S.Carrier,
    S.RateThickDomain p →
    S.RankRateNonNull p

/-- The concrete λ-thick simplex has a rank-rate non-null witness by construction. -/
theorem simplex_rateThickRankRateNonNullWitness
    (m : Nat) (lam : Real) :
    RateThickRankRateNonNullWitnessConcrete
      (SimplexChronosState m lam) := by
  intro p hp
  trivial

/--
Coercivity plus rank-rate non-null witness gives the positive entropy lower bound.

This is a concrete theorem-interface bridge only.
-/
theorem positiveEntropyLowerBound_from_coercivity_and_rankWitness
    (S : ChronosThickState)
    {eta : Real}
    (hcoercive : RateThickFiberCoercivityConcrete S eta)
    (_hwitness : RateThickRankRateNonNullWitnessConcrete S) :
    RateThickPositiveEntropyLowerBoundConcrete S eta := by
  intro p hp _hnonnull
  exact hcoercive.2 p hp

/-- The concrete λ-thick simplex has the positive entropy lower bound from certificate plus witness. -/
theorem simplex_positiveEntropyLowerBound_from_certificate_and_rankWitness
    (m : Nat) (lam : Real)
    (hm : 2 ≤ m)
    (hlam_pos : 0 < lam)
    (hlam_le : lam ≤ (1 : Real) / m)
    (cert : SimplexEntropyCertificate m lam) :
    RateThickPositiveEntropyLowerBoundConcrete
      (SimplexChronosState m lam)
      (simplexEta m lam) := by
  exact positiveEntropyLowerBound_from_coercivity_and_rankWitness
    (SimplexChronosState m lam)
    (SimplexEntropyCoercivityAxiom.simplex_rateThickFiberCoercivity
      m lam hm hlam_pos hlam_le cert)
    (simplex_rateThickRankRateNonNullWitness m lam)

end

end RateThickRankRateNonNullWitnessTheorem
end Frontier
end Chronos
