import CLR.FiniteGraph
import CLR.FOSyntax

universe u

namespace CLR

def Pebbling (α : Type u) (k : Nat) := Fin k → Option α

structure Position (G H : FiniteGraph) (k : Nat) where
  left : Pebbling G.V k
  right : Pebbling H.V k

def PartialIso {G H : FiniteGraph} {k : Nat} (p : Position G H k) : Prop :=
  (∀ i, (p.left i).isSome ↔ (p.right i).isSome) ∧
  (∀ i j,
    match p.left i, p.left j, p.right i, p.right j with
    | some a, some b, some c, some d =>
        (a = b ↔ c = d) ∧ (G.adj a b ↔ H.adj c d)
    | none, none, none, none => True
    | _, _, _, _ => False)

inductive EFWin : Nat → {k : Nat} → (G H : FiniteGraph) → Prop
  | zero {k} {G H} : PartialIso {G := G} {H := H}
      { left := fun _ => none, right := fun _ => none } → EFWin 0 (k := k) G H
  | succL {q k} {G H} :
      (∀ a : G.V, ∃ b : H.V, EFWin q (k := k) G H) → EFWin (q + 1) (k := k) G H
  | succR {q k} {G H} :
      (∀ b : H.V, ∃ a : G.V, EFWin q (k := k) G H) → EFWin (q + 1) (k := k) G H

def foEquiv (k q : Nat) (G H : FiniteGraph) : Prop := EFWin q (k := k) G H

end CLR
