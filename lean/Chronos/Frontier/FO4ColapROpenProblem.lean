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

theorem not_fo4CycleOverlapRankBoundProblem :
    ¬ FO4CycleOverlapRankBoundProblem := by
  intro hProblem
  rcases hProblem 0 0 with ⟨C, hC⟩
  let G : GraphDatum :=
    { vertex := Unit
      adj := fun _ _ => False }
  let X : FO4HomogeneousInput :=
    { Delta := 0
      R := 0
      G := G
      degree_bounded := True
      radius_R_FO4_indistinguishable := True }
  have hHom : FO4Homogeneous X := ⟨trivial, trivial⟩
  let w : RadiusRCycleWitness G :=
    { center := ()
      support := fun _ => False
      radius_R_local := True
      cycle_witness := True }
  let inc : CycleOverlapIncidence G 0 :=
    { left := w
      right := w
      overlaps_within_radius := True }
  let ρ : ColapR X.G X.R :=
    { coeff := fun _ => F2.zero
      finite_support := True
      rank := C + 1
      basisWitness := fun _ => inc }
  have hbad : C + 1 ≤ C := by
    simpa [ρ] using hC X rfl rfl hHom ρ
  exact Nat.not_succ_le_self C hbad

def FrontierStatus : String :=
  "FORMAL_SURFACE_REFUTED_UNCONSTRAINED_RANK"

def ClosedSurface : String :=
  "The current ColapR rank-bound problem is refuted because rank is an unconstrained Nat independent of the coefficient data."

def MissingLemma : String :=
  "CanonicalCorrectedColapRank: derive rank from finite-dimensional F2 overlap data after quotienting local repetition; the present arbitrary rank field cannot support a sound rigidity theorem."

def Boundary : String :=
  "Refutes only the current repository-native formal surface. It does not by itself formalize the torus counterexample or prove a replacement Oblivion theorem, P vs NP, or any Clay problem."

end FO4ColapROpenProblem
end Frontier
end Chronos
