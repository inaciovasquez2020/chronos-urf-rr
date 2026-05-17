import Chronos.Frontier.RateThickRankRateNonNullWitnessTheorem

namespace Chronos
namespace Frontier
namespace RateThickFiberEntropyGapTheorem

open SimplexEntropyCoercivityAxiom
open RateThickFiberCoercivityTheorem
open RateThickRankRateNonNullWitnessTheorem

noncomputable section

/-- Concrete rate-thick fiber entropy gap on a rate-thick Chronos state. -/
def RateThickFiberEntropyGapConcrete
    (S : ChronosThickState)
    (eta : Real) : Prop :=
  0 < eta ∧
  ∀ p : S.Carrier,
    S.RateThickDomain p →
    S.RankRateNonNull p →
    eta ≤ S.FiberEntropyMass p

/-- Coercivity plus rank-rate non-null witness proves the concrete fiber entropy gap. -/
theorem rateThickFiberEntropyGap_from_coercivity_and_rankWitness
    (S : ChronosThickState)
    {eta : Real}
    (hcoercive : RateThickFiberCoercivityConcrete S eta)
    (_hwitness : RateThickRankRateNonNullWitnessConcrete S) :
    RateThickFiberEntropyGapConcrete S eta := by
  constructor
  · exact hcoercive.1
  · intro p hp _hnonnull
    exact hcoercive.2 p hp

/-- Positive entropy lower bound plus eta positivity proves the concrete fiber entropy gap. -/
theorem rateThickFiberEntropyGap_from_positiveEntropyLowerBound
    (S : ChronosThickState)
    {eta : Real}
    (heta : 0 < eta)
    (hpos : RateThickPositiveEntropyLowerBoundConcrete S eta) :
    RateThickFiberEntropyGapConcrete S eta := by
  constructor
  · exact heta
  · intro p hp hnonnull
    exact hpos p hp hnonnull

/--
The concrete λ-thick simplex has a rate-thick fiber entropy gap from:
1. the explicit simplex entropy certificate;
2. the rank-rate non-null witness interface.
-/
theorem simplex_rateThickFiberEntropyGap_from_certificate_and_rankWitness
    (m : Nat) (lam : Real)
    (hm : 2 ≤ m)
    (hlam_pos : 0 < lam)
    (hlam_le : lam ≤ (1 : Real) / m)
    (cert : SimplexEntropyCertificate m lam) :
    RateThickFiberEntropyGapConcrete
      (SimplexChronosState m lam)
      (simplexEta m lam) := by
  exact rateThickFiberEntropyGap_from_coercivity_and_rankWitness
    (SimplexChronosState m lam)
    (SimplexEntropyCoercivityAxiom.simplex_rateThickFiberCoercivity
      m lam hm hlam_pos hlam_le cert)
    (RateThickRankRateNonNullWitnessTheorem.simplex_rateThickRankRateNonNullWitness
      m lam)

/--
Equivalent direct certificate route:
the certificate supplies eta positivity and entropy lower bound directly.
-/
theorem simplex_rateThickFiberEntropyGap_from_certificate
    (m : Nat) (lam : Real)
    (hm : 2 ≤ m)
    (hlam_pos : 0 < lam)
    (hlam_le : lam ≤ (1 : Real) / m)
    (cert : SimplexEntropyCertificate m lam) :
    RateThickFiberEntropyGapConcrete
      (SimplexChronosState m lam)
      (simplexEta m lam) := by
  constructor
  · exact cert.eta_pos hm hlam_pos hlam_le
  · intro p hp _hnonnull
    exact cert.entropy_min hm hlam_pos hlam_le p hp.1 hp.2

end

end RateThickFiberEntropyGapTheorem
end Frontier
end Chronos
