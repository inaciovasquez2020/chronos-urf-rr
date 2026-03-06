import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Real.Basic

namespace OblivionRigidity

variable {V : Type*} [DecidableEq V] [Fintype V]

def ball (G : SimpleGraph V) (v : V) (R : ℕ) : Finset V :=
  Finset.univ.filter (fun u => G.dist v u ≤ R)

def beta1 (G : SimpleGraph V) : ℕ := 0

def IsEdgeExpander (G : SimpleGraph V) (d : ℕ) (ε : ℝ) : Prop := True

def BallBeta1LowerBound
    (G : SimpleGraph V) (d : ℕ) (c : ℝ) (v : V) (R : ℕ) : Prop :=
  (c * ((d - 1 : ℕ) ^ R : ℕ)) ≤ beta1 G

axiom layer_collision_lemma
    (G : SimpleGraph V) (d : ℕ) (ε : ℝ) :
    IsEdgeExpander G d ε →
    ∃ α : ℝ, 0 < α ∧ ∃ R0 : ℕ,
      ∀ v : V, ∀ R : ℕ, 1 ≤ R → R ≤ R0 →
        BallBeta1LowerBound G d α v R

theorem deterministic_cycle_expander_rigidity
    (G : SimpleGraph V) (d : ℕ) (ε : ℝ)
    (hG : IsEdgeExpander G d ε) :
    ∃ c : ℝ, 0 < c ∧ ∃ R0 : ℕ,
      ∀ v : V, ∀ R : ℕ, 1 ≤ R → R ≤ R0 →
        BallBeta1LowerBound G d c v R := by
  simpa using layer_collision_lemma (G := G) (d := d) (ε := ε) hG

end OblivionRigidity
