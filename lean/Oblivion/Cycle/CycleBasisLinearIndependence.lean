import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix
import Mathlib.LinearAlgebra.FiniteDimensional
import Mathlib.LinearAlgebra.LinearIndependent
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

namespace Oblivion

open Matrix

abbrev F2 := ZMod 2

universe u

structure CycleSystem where
  cycles : Type u
  edges  : Type u
  mem    : cycles → edges → Prop

namespace CycleSystem

variable (S : CycleSystem)

def incidenceMatrix [Fintype S.cycles] [Fintype S.edges] :
  Matrix S.edges S.cycles F2 :=
  fun e c => if S.mem c e then 1 else 0

def incidenceColumn [Fintype S.cycles] [Fintype S.edges] (c : S.cycles) :
  S.edges → F2 :=
  fun e => S.incidenceMatrix e c

def cycleRank [Fintype S.cycles] [Fintype S.edges] : Nat :=
  (S.incidenceMatrix).rank

def incidenceColumns [Fintype S.cycles] [Fintype S.edges] (B : Finset S.cycles) :
  S.cycles → S.edges → F2 :=
  fun c => S.incidenceColumn c

theorem cycle_basis_linear_independence_bound
  [Fintype S.cycles] [Fintype S.edges]
  (B : Finset S.cycles)
  (hlin : LinearIndependent F2 (fun c : B => S.incidenceColumn c)) :
  B.card ≤ S.cycleRank := by
  classical
  let W : Submodule F2 (S.edges → F2) := Matrix.colSpace (S.incidenceMatrix)
  have hsub : Submodule.span F2 (Set.range (fun c : B => S.incidenceColumn c)) ≤ W := by
    intro x hx
    refine Submodule.span_induction hx ?hbase ?hzero ?hadd ?hsmul
    · intro y hy
      rcases hy with ⟨c, rfl⟩
      change S.incidenceColumn (c : S.cycles) ∈ W
      exact Matrix.subset_span (by
        refine ⟨(c : S.cycles), ?_⟩
        ext e
        rfl)
    · exact W.zero_mem
    · intro x y hx hy
      exact W.add_mem hx hy
    · intro a x hx
      exact W.smul_mem a hx
  have hfinrank_le :
      Module.finrank F2 (Submodule.span F2 (Set.range (fun c : B => S.incidenceColumn c))) ≤
      Module.finrank F2 W := by
    exact FiniteDimensional.finrank_mono hsub
  have hcard_eq :
      B.card =
      Module.finrank F2 (Submodule.span F2 (Set.range (fun c : B => S.incidenceColumn c))) := by
    simpa using LinearIndependent.finset_card_eq_finrank_span hlin
  have hrank_eq : Module.finrank F2 W = S.cycleRank := by
    simp [W, cycleRank]
  rw [hcard_eq, hrank_eq]
  exact hfinrank_le

theorem cycle_basis_linear_independence_bound_univ
  [Fintype S.cycles] [Fintype S.edges]
  (hlin : LinearIndependent F2 (fun c : S.cycles => S.incidenceColumn c)) :
  Fintype.card S.cycles ≤ S.cycleRank := by
  classical
  simpa using
    (S.cycle_basis_linear_independence_bound (Finset.univ) (by
      simpa using hlin))

end CycleSystem

end Oblivion
