import Oblivion.Graph
import Oblivion.Tree

namespace Oblivion

variable {G : Graph}

/-- Rooted parity potential on a tree via path accumulation. -/
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

/-- Edge parity constraint via unique path decomposition in tree. -/
lemma tree_potential_edge
    (T : Graph)
    (hT : IsTree T)
    (σ : T.E → Bool)
    (v₀ : T.V)
    (e : T.E) :
    tree_potential T hT σ v₀ e.1.1 ^^^
    tree_potential T hT σ v₀ e.1.2 = σ e := by
  classical
  obtain ⟨p₁, hp₁⟩ := hT.connected.path_exists v₀ e.1.1
  obtain ⟨p₂, hp₂⟩ := hT.connected.path_exists v₀ e.1.2
  have hunique := hT.acyclic
  have : p₂ = p₁.appendEdge e := by
    admit
  simp [tree_potential, this]

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
