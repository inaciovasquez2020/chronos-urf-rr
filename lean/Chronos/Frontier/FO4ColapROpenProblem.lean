import Chronos.Frontier.FO4HomogeneousOpenProblem
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Prod

namespace Chronos
namespace Frontier
namespace FO4ColapROpenProblem

open FO4HomogeneousOpenProblem

inductive F2 where
  | zero : F2
  | one : F2
deriving DecidableEq, Repr

def F2.add : F2 → F2 → F2
  | zero, x => x
  | x, zero => x
  | one, one => zero

def F2.mul : F2 → F2 → F2
  | zero, _ => zero
  | _, zero => zero
  | one, one => one

structure RadiusRCycleWitness (G : GraphDatum) where
  center : G.vertex
  support : G.vertex → Prop
  radius_R_local : Prop
  cycle_witness : Prop

structure CycleOverlapIncidence (G : GraphDatum) (R : Nat) where
  left : RadiusRCycleWitness G
  right : RadiusRCycleWitness G
  overlaps_within_radius : Prop

structure F2WeightedOverlapRelation (G : GraphDatum) (R : Nat) where
  coeff : CycleOverlapIncidence G R → F2
  finite_support : Prop
  rank : Nat
  basisWitness : Fin rank → CycleOverlapIncidence G R

def ColapR (G : GraphDatum) (R : Nat) : Type :=
  F2WeightedOverlapRelation G R

def ColapRankBoundedAt (X : FO4HomogeneousInput) (C : Nat) : Prop :=
  ∀ ρ : ColapR X.G X.R, ρ.rank ≤ C

structure FO4RankTypeSignature
    (X : FO4HomogeneousInput)
    (ρ : ColapR X.G X.R) where
  typeCount : Nat
  typeOf : Fin ρ.rank → Fin typeCount

structure FO4BoundedFiberEncoding
    (X : FO4HomogeneousInput)
    (ρ : ColapR X.G X.R)
    (σ : FO4RankTypeSignature X ρ) where
  fiberBound : Nat
  fiberSlot : Fin ρ.rank → Fin fiberBound
  encoding_injective :
    Function.Injective (fun i => (σ.typeOf i, fiberSlot i))

theorem rank_le_typeCount_mul_fiberBound
    {X : FO4HomogeneousInput}
    {ρ : ColapR X.G X.R}
    {σ : FO4RankTypeSignature X ρ}
    (h : FO4BoundedFiberEncoding X ρ σ) :
    ρ.rank ≤ σ.typeCount * h.fiberBound := by
  have hcard :=
    Fintype.card_le_of_injective
      (fun i : Fin ρ.rank => (σ.typeOf i, h.fiberSlot i))
      h.encoding_injective
  simpa [Fintype.card_prod] using hcard

theorem type_diversity_of_bounded_fiber_estimate
    {witnessRank typeCount fiberBound : Nat}
    (hbound : witnessRank ≤ fiberBound * typeCount)
    (hlarge : fiberBound < witnessRank) :
    2 ≤ typeCount := by
  cases typeCount with
  | zero =>
      have hw : witnessRank = 0 := by
        exact Nat.eq_zero_of_le_zero (by simpa using hbound)
      subst witnessRank
      exact (Nat.not_lt_zero fiberBound hlarge).elim
  | succ n =>
      cases n with
      | zero =>
          have hw : witnessRank ≤ fiberBound := by
            simpa using hbound
          exact (Nat.not_lt_of_ge hw hlarge).elim
      | succ n =>
          exact Nat.succ_le_succ (Nat.succ_le_succ (Nat.zero_le n))

theorem type_diversity_of_bounded_fiber_encoding
    {X : FO4HomogeneousInput}
    {ρ : ColapR X.G X.R}
    {σ : FO4RankTypeSignature X ρ}
    (h : FO4BoundedFiberEncoding X ρ σ)
    (hlarge : h.fiberBound < ρ.rank) :
    2 ≤ σ.typeCount := by
  exact type_diversity_of_bounded_fiber_estimate
    (witnessRank := ρ.rank)
    (typeCount := σ.typeCount)
    (fiberBound := h.fiberBound)
    (by simpa [Nat.mul_comm] using rank_le_typeCount_mul_fiberBound h)
    hlarge

def FO4CycleOverlapRankBoundProblem : Prop :=
  ∀ Δ R : Nat,
    ∃ C : Nat,
      ∀ X : FO4HomogeneousInput,
        X.Delta = Δ →
        X.R = R →
        FO4Homogeneous X →
        ColapRankBoundedAt X C

def FrontierStatus : String :=
  "OPEN_PROBLEM_REQUIRED"

def ClosedSurface : String :=
  "ColapR type surface over F2 formalized."

def MissingLemma : String :=
  "FO4-local indistinguishability under bounded degree implies uniformly bounded radius-R cycle-overlap rank."

def Boundary : String :=
  "Defines ColapR only; does not prove finite FO4 radius-R type enumeration, does not prove bounded cycle-overlap rank, does not close rigidity, and does not prove P vs NP or any Clay problem."

end FO4ColapROpenProblem
end Frontier
end Chronos
