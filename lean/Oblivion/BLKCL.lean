import Oblivion.CodeR
import Oblivion.BlockInjectiveAssumption

universe u

open Classical

variable {G : Graph}
variable [Fintype G.V] [Fintype G.E]
variable [DecidableEq G.V] [DecidableEq G.E]

def parent (G : Graph) (v : G.V) (i : Nat) (x : G.V) : G.V :=
  Option.getD (parentChoice G v i x) x

axiom BLKCL_bridge
  (G : Graph)
  [Fintype G.V] [Fintype G.E]
  [DecidableEq G.V] [DecidableEq G.E]
  (R i : Nat) (v : G.V) :
  ∀ {x y : G.V},
    x ∈ Layer G v i →
    y ∈ Layer G v i →
    (parentChoice G v i x,
     edgeLabel G (parent G v i x) x)
    =
    (parentChoice G v i y,
     edgeLabel G (parent G v i y) y)
    →
    x = y

theorem BLKCL := BLKCL_bridge

theorem BLKCL_implies_block_injective
  (R i : Nat) (v : G.V) :
  ∀ {x y : G.V},
    x ∈ Layer G v i →
    y ∈ Layer G v i →
    (parent G v i x,
     edgeLabel G (parent G v i x) x)
    =
    (parent G v i y,
     edgeLabel G (parent G v i y) y)
    →
    x = y :=
by
  intro x y hx hy h
  have h' :
    (parentChoice G v i x,
     edgeLabel G (parent G v i x) x)
    =
    (parentChoice G v i y,
     edgeLabel G (parent G v i y) y) := by
    cases parentChoice G v i x <;> cases parentChoice G v i y <;> simp [parent] at h ⊢
  exact BLKCL_bridge G R i v hx hy h'
