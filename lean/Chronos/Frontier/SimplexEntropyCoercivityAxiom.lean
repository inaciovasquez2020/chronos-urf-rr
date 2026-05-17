import Chronos.Frontier.RateThickFiberCoercivityTheorem
import Mathlib

namespace Chronos
namespace Frontier
namespace SimplexEntropyCoercivityAxiom

open scoped BigOperators
open RateThickFiberCoercivityTheorem

noncomputable section

/-- Explicit entropy floor on the λ-thick simplex. -/
def simplexEta (m : Nat) (lam : Real) : Real :=
  - ((1 - ((m : Real) - 1) * lam) * Real.log (1 - ((m : Real) - 1) * lam))
  - (((m : Real) - 1) * lam * Real.log lam)

/-- Shannon entropy on `Fin m → Real`. -/
def simplexEntropy (m : Nat) (p : Fin m → Real) : Real :=
  - (∑ i, p i * Real.log (p i))

/-- λ-thick simplex predicate. -/
def ThickSimplex (m : Nat) (lam : Real) (p : Fin m → Real) : Prop :=
  (∀ i, lam ≤ p i) ∧ ∑ i, p i = 1

/--
Explicit analytic certificate for entropy coercivity on the thick simplex.

This removes hidden `sorry` declarations from this file.
The analytic payload is now an explicit input.
-/
structure SimplexEntropyCertificate (m : Nat) (lam : Real) where
  eta_pos :
    2 ≤ m →
    0 < lam →
    lam ≤ (1 : Real) / m →
    0 < simplexEta m lam
  entropy_min :
    2 ≤ m →
    0 < lam →
    lam ≤ (1 : Real) / m →
    ∀ p : Fin m → Real,
      (∀ i, lam ≤ p i) →
      (∑ i, p i = 1) →
      simplexEta m lam ≤ simplexEntropy m p

/-- The concrete λ-thick simplex Chronos state. -/
def SimplexChronosState (m : Nat) (lam : Real) :
    ChronosThickState where
  Carrier := Fin m → Real
  RateThickDomain := ThickSimplex m lam
  FiberEntropyMass := simplexEntropy m
  RankRateNonNull := fun _ => True

/-- The entropy certificate gives an explicit lower-bound datum. -/
def simplex_entropyLowerBoundDatum
    (m : Nat) (lam : Real)
    (hm : 2 ≤ m)
    (hlam_pos : 0 < lam)
    (hlam_le : lam ≤ (1 : Real) / m)
    (cert : SimplexEntropyCertificate m lam) :
    EntropyLowerBoundDatum (SimplexChronosState m lam) :=
  {
    eta := simplexEta m lam
    eta_pos := cert.eta_pos hm hlam_pos hlam_le
    entropy_lower := by
      intro p hp
      exact cert.entropy_min hm hlam_pos hlam_le p hp.1 hp.2
  }

/-- The concrete λ-thick simplex satisfies rate-thick fiber coercivity from the certificate. -/
theorem simplex_rateThickFiberCoercivity
    (m : Nat) (lam : Real)
    (hm : 2 ≤ m)
    (hlam_pos : 0 < lam)
    (hlam_le : lam ≤ (1 : Real) / m)
    (cert : SimplexEntropyCertificate m lam) :
    RateThickFiberCoercivityConcrete
      (SimplexChronosState m lam)
      (simplexEta m lam) := by
  constructor
  · exact cert.eta_pos hm hlam_pos hlam_le
  · intro p hp
    exact cert.entropy_min hm hlam_pos hlam_le p hp.1 hp.2

/-- The concrete λ-thick simplex satisfies the positive entropy lower bound from the certificate. -/
theorem simplex_rateThickPositiveEntropyLowerBound
    (m : Nat) (lam : Real)
    (hm : 2 ≤ m)
    (hlam_pos : 0 < lam)
    (hlam_le : lam ≤ (1 : Real) / m)
    (cert : SimplexEntropyCertificate m lam) :
    RateThickPositiveEntropyLowerBoundConcrete
      (SimplexChronosState m lam)
      (simplexEta m lam) := by
  intro p hp _hnonnull
  exact cert.entropy_min hm hlam_pos hlam_le p hp.1 hp.2

end

end SimplexEntropyCoercivityAxiom
end Frontier
end Chronos
