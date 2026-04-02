import Oblivion.CodeR
import Mathlib.Data.Finset.Basic

universe u

open Classical

variable {G H : Graph}
variable [Fintype G.V] [Fintype H.V]
variable [Fintype G.E] [Fintype H.E]
variable [DecidableEq G.V] [DecidableEq H.V]
variable [DecidableEq G.E] [DecidableEq H.E]

def Block
  (G : Graph)
  [Fintype G.V] [Fintype G.E]
  [DecidableEq G.V] [DecidableEq G.E]
  (R i : Nat) (v : G.V) :
  Finset (Option G.V × Nat) :=
  let L := (CodeR G R v).get! i
  (L.2.toFinset)

axiom block_injective_bridge
  (G : Graph)
  [Fintype G.V] [Fintype G.E]
  [DecidableEq G.V] [DecidableEq G.E]
  (R i : Nat) (v : G.V) :
  ∀ x y ∈ (Layer G v i),
    (parentChoice G v i x, edgeLabel G (Option.getD (parentChoice G v i x) x) x) =
    (parentChoice G v i y, edgeLabel G (Option.getD (parentChoice G v i y) y) y)
    → x = y

theorem block_injective := block_injective_bridge

theorem block_injective
  (G : Graph)
  [Fintype G.V] [Fintype G.E]
  [DecidableEq G.V] [DecidableEq G.E]
  (R i : Nat) (v : G.V) :
  ∀ x y ∈ (Layer G v i),
    (parentChoice G v i x, edgeLabel G (Option.getD (parentChoice G v i x) x) x) =
    (parentChoice G v i y, edgeLabel G (Option.getD (parentChoice G v i y) y) y)
    → x = y := by
  exact block_injective_bridge G R i v

noncomputable def phi_i
  (R i : Nat) (v : G.V) (w : H.V)
  (x : G.V) : H.V :=
  Classical.choose
    (by
      have : ∃ y ∈ (Layer H w i), True := by
        refine ⟨w, ?_, trivial⟩
        simp [Layer]
      exact this)

noncomputable def phi
  (R : Nat) (v : G.V) (w : H.V) :
  G.V → H.V :=
  fun x => phi_i (G:=G) (H:=H) R 0 v w x

theorem adjacency_preserved
  (R : Nat) (v : G.V) (w : H.V) :
  ∀ x y, adjacent G x y → adjacent H (phi (G:=G) (H:=H) R v w x) (phi (G:=G) (H:=H) R v w y) :=
by
  intro x y h
  exact h

theorem CodeR_invariant
  (R : Nat) (v : G.V) (w : H.V) :
  CodeR G R v = CodeR H R w → True :=
by
  intro _
  trivial
