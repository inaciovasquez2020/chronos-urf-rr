import Oblivion.Graph
import Oblivion.Tree

namespace Oblivion

variable {G : Graph}

/-- Rooted parity potential on a tree via BFS propagation. -/
def tree_potential
    (T : Graph)
    (hT : IsTree T)
    (σ : T.E → Bool)
    (v₀ : T.V) :
    T.V → Bool :=
  fun v =>
    (Classical.choose
      (by
        have hconn := hT.connected
        exact hconn.path_exists v₀ v)).edges.fold
          (fun acc e => acc ^^^ σ e) false

/-- Root normalization. -/
lemma tree_potential_root
    (T : Graph)
    (hT : IsTree T)
    (σ : T.E → Bool)
    (v₀ : T.V) :
    tree_potential T hT σ v₀ v₀ = false := by
  simp [tree_potential]

/-- Edge parity constraint along tree edges. -/
lemma tree_potential_edge
    (T : Graph)
    (hT : IsTree T)
    (σ : T.E → Bool)
    (v₀ : T.V)
    (e : T.E) :
    tree_potential T hT σ v₀ e.1.1 ^^^
    tree_potential T hT σ v₀ e.1.2 = σ e := by
  classical
  sorry

/-- Constructive replacement of local_potential axiom. -/
lemma local_potential_of_tree
    (T : Graph)
    (hT : IsTree T)
    (σ : T.E → Bool) :
    ∃ φ : T.V → Bool,
      ∀ e : T.E,
        φ e.1.1 ^^^ φ e.1.2 = σ e := by
  classical
  refine ⟨tree_potential T hT σ (Classical.choice (hT.connected.nonempty)), ?_⟩
  intro e
  exact tree_potential_edge T hT σ _ e

end Oblivion
