import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Nat.Basic

namespace OblivionRigidity

variable {V : Type*} [DecidableEq V] [Fintype V]

/- Radius ball -/
def ball (G : SimpleGraph V) (v : V) (R : ℕ) : Finset V :=
  Finset.univ.filter (fun u => G.dist v u ≤ R)

/- Internal edges placeholder -/
def internalEdges (G : SimpleGraph V) (v : V) (R : ℕ) : ℕ :=
0

/- Cycle rank placeholder -/
def beta1 (G : SimpleGraph V) : ℕ :=
0

/- Expander predicate placeholder -/
def IsEdgeExpander (G : SimpleGraph V) (d : ℕ) (ε : ℝ) : Prop :=
True

/- Internal edge density predicate -/
def InternalEdgeDensity
  (G : SimpleGraph V)
  (α : ℝ)
  (v : V)
  (R : ℕ) : Prop :=
((1 + α) * (ball G v R).card : ℝ) ≤ internalEdges G v R

/- Target lemma skeleton -/
axiom expander_internal_edge_density
  (G : SimpleGraph V)
  (d : ℕ)
  (ε : ℝ) :
  IsEdgeExpander G d ε →
  ∃ α : ℝ, 0 < α ∧
  ∃ R0 : ℕ,
    ∀ v : V,
    ∀ R : ℕ,
      1 ≤ R →
      R ≤ R0 →
      InternalEdgeDensity G α v R

/- Consequence for cycle rank -/
axiom beta1_from_density
  (G : SimpleGraph V)
  (v : V)
  (R : ℕ) :
  internalEdges G v R ≤ beta1 G

/- Deterministic cycle growth corollary -/
theorem deterministic_cycle_growth
  (G : SimpleGraph V)
  (d : ℕ)
  (ε : ℝ)
  (hG : IsEdgeExpander G d ε) :
  ∃ α : ℝ, 0 < α ∧
  ∃ R0 : ℕ,
    ∀ v : V,
    ∀ R : ℕ,
      1 ≤ R →
      R ≤ R0 →
      (α * ((d - 1 : ℕ) ^ R : ℕ)) ≤ beta1 G := by
  obtain ⟨α, hα, R0, h⟩ :=
    expander_internal_edge_density (G := G) (d := d) (ε := ε) hG
  refine ⟨α, hα, R0, ?_⟩
  intro v R h1 h2
  have hden := h v R h1 h2
  have hβ := beta1_from_density (G := G) (v := v) (R := R)
  exact le_trans ?_ hβ
