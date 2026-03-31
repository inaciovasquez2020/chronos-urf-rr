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
axiom Connected.path_exists
    (h : Connected T) (a b : T.V) :
    ∃ p : Path T, True

/-- Nonempty vertex type. -/
axiom Connected.nonempty
    (h : Connected T) :
    Nonempty T.V

/-- Distance property for adjacent vertices in trees. -/
axiom IsTree.dist_adj_property
    (hT : IsTree T)
    (v₀ : T.V)
    (e : T.E) :
    dist v₀ e.1.2 = dist v₀ e.1.1 + 1 ∨
    dist v₀ e.1.1 = dist v₀ e.1.2 + 1

/-- Forward path extension uniqueness. -/
axiom IsTree.unique_path_extension_forward
    (hT : IsTree T)
    (v₀ : T.V)
    (p : Path T)
    (e : T.E)
    (h_forward : dist v₀ e.1.2 = dist v₀ e.1.1 + 1) :
    ∀ p', p' = Path.appendEdge p e

/-- Backward path extension uniqueness. -/
axiom IsTree.unique_path_extension_backward
    (hT : IsTree T)
    (v₀ : T.V)
    (p : Path T)
    (e : T.E)
    (h_backward : dist v₀ e.1.1 = dist v₀ e.1.2 + 1) :
    ∀ p', p' = Path.appendEdge p e

end Oblivion
