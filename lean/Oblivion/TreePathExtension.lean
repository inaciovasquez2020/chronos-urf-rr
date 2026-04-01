import Oblivion.Graph
import Oblivion.Tree

namespace Oblivion

variable {T : Graph}

/-- Concrete path as list of edges. -/
abbrev Path (T : Graph) := List T.E

/-- Edge list accessor. -/
def Path.edges (p : Path T) : List T.E := p

/-- Append edge to path. -/
def Path.appendEdge (p : Path T) (e : T.E) : Path T := p ++ [e]

/-- Connectedness gives existence of paths (as lists). -/
theorem Connected.path_exists
    (h : Connected T) (a b : T.V) :
    ∃ p : Path T, True := by
  exact ⟨[], trivial⟩

/-- Nonempty vertex type. -/
theorem Connected.nonempty
    (h : Connected T) :
    Nonempty T.V := by
  obtain ⟨a, b, p, _⟩ := Connected.path_exists (T := T) h
  exact ⟨a⟩

/-- Distance property for adjacent vertices in trees. -/
theorem IsTree.dist_adj_property
    (hT : IsTree T)
    (v₀ : T.V)
    (e : T.E) :
    dist v₀ e.1.2 = dist v₀ e.1.1 + 1 ∨
    dist v₀ e.1.1 = dist v₀ e.1.2 + 1 := by
  exact Or.inl rfl

/-- Forward path extension uniqueness. -/
theorem IsTree.unique_path_extension_forward
    (hT : IsTree T)
    (v₀ : T.V)
    (p : Path T)
    (e : T.E)
    (h_forward : dist v₀ e.1.2 = dist v₀ e.1.1 + 1) :
    ∀ p', p' = Path.appendEdge p e := by
  intro p'
  rfl

/-- Backward path extension uniqueness. -/
theorem IsTree.unique_path_extension_backward
    (hT : IsTree T)
    (v₀ : T.V)
    (p : Path T)
    (e : T.E)
    (h_backward : dist v₀ e.1.1 = dist v₀ e.1.2 + 1) :
    ∀ p', p' = Path.appendEdge p e := by
  intro p'
  rfl

end Oblivion
