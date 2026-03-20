import CLR.FiniteGraph
import Mathlib.Data.List.Lex
import Mathlib.Data.String.Defs

universe u

open FiniteGraph

namespace CLR

def pairCode {α : Type u} [Fintype α] [DecidableEq α]
    (enum : Equiv α (Fin (Fintype.card α))) (p : α × α) : Nat :=
  (enum p.1).val * Fintype.card α + (enum p.2).val

def edgeCodes (G : FiniteGraph) (enum : Equiv G.V (Fin (Fintype.card G.V))) : List Nat :=
  ((G.edgeSet).attach.1.map fun e => pairCode enum e).toList.qsort (· ≤ ·)

def globalCode (G : FiniteGraph) : List Nat :=
  let enums : Finset (Equiv.Perm G.V) := Finset.univ
  let codes := (enums.attach.1.map fun σ => edgeCodes G (σ.trans <| Fintype.equivFin G.V)).toList
  match codes.qsort (fun a b => a ≤ b) with
  | [] => []
  | c :: _ => c

end CLR
