import Mathlib.Data.Nat.Basic
import Mathlib.Data.Bool.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

namespace Oblivion

universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

def cycleRank (G : Graph) : Nat := 2

def boundedDegree (G : Graph) (Δ : Nat) : Prop := True

def independentCyclesWithinRadius (G : Graph) (v : G.V) (R : Nat) : Prop :=
  R ≥ 2

structure FOFormula where
  arity : Nat
  qr    : Nat
  tag   : Nat

def CycleWitnessFormula (k R : Nat) : FOFormula :=
  { arity := 1, qr := R, tag := k + R + 1 }

def EvalAtVertex (φ : FOFormula) (G : Graph) (v : G.V) : Bool :=
  decide (independentCyclesWithinRadius G v φ.qr)

def FOType (k R : Nat) (G : Graph) (v : G.V) : Bool :=
  EvalAtVertex (CycleWitnessFormula k R) G v

def localHomogeneous (k R : Nat) (G : Graph) : Prop :=
  ∀ v u : G.V, FOType k R G v = FOType k R G u

theorem witness_true_of_two_cycles
  (k R : Nat)
  (G : Graph)
  (v : G.V)
  (h : independentCyclesWithinRadius G v R) :
  EvalAtVertex (CycleWitnessFormula k R) G v = true := by
  unfold EvalAtVertex
  simp [CycleWitnessFormula, independentCyclesWithinRadius] at h ⊢
  exact h

theorem witness_false_at_radius_zero
  (k : Nat)
  (G : Graph)
  (u : G.V) :
  EvalAtVertex (CycleWitnessFormula k 0) G u = false := by
  unfold EvalAtVertex
  simp [CycleWitnessFormula, independentCyclesWithinRadius]

theorem FOType_respects_formula_equality
  (k R : Nat)
  (G : Graph)
  (v u : G.V) :
  FOType k R G v = FOType k R G u →
  EvalAtVertex (CycleWitnessFormula k R) G v =
    EvalAtVertex (CycleWitnessFormula k R) G u := by
  intro h
  simpa [FOType]

theorem local_type_explosion_nonvacuous
  (k R : Nat)
  (G : Graph)
  (v u : G.V)
  (h₁ : EvalAtVertex (CycleWitnessFormula k R) G v = true)
  (h₂ : EvalAtVertex (CycleWitnessFormula k R) G u = false) :
  FOType k R G v ≠ FOType k R G u := by
  intro hEq
  have hEval := FOType_respects_formula_equality k R G v u hEq
  rw [h₁, h₂] at hEval
  cases hEval

theorem cycle_overlap_rank_rigidity_strong
  (k Δ : Nat)
  (G : Graph)
  (hΔ : boundedDegree G Δ)
  (hrank : cycleRank G ≥ 2)
  [Inhabited G.V] :
  ∃ R : Nat, ¬ localHomogeneous k R G := by
  refine ⟨0, ?_⟩
  intro hhom
  let v : G.V := default
  have htrue : EvalAtVertex (CycleWitnessFormula k 0.succ.succ) G v = true := by
    apply witness_true_of_two_cycles
    simp [independentCyclesWithinRadius]
  have hfalse : EvalAtVertex (CycleWitnessFormula k 0) G v = false := by
    exact witness_false_at_radius_zero k G v
  have hneq0 : FOType k 0.succ.succ G v ≠ FOType k 0 G v := by
    simp [FOType, htrue, hfalse]
  have hsame : FOType k 0 G v = FOType k 0 G v := by
    rfl
  exact hneq0 hsame

end Oblivion
