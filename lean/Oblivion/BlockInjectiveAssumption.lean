import Oblivion.CodeR

universe u

open Classical

variable {G : Graph}
variable [Fintype G.V] [Fintype G.E]
variable [DecidableEq G.V] [DecidableEq G.E]

def parent (G : Graph) (v : G.V) (i : Nat) (x : G.V) : G.V :=
  Option.getD (parentChoice G v i x) x

theorem block_injective_bridge
  (G : Graph)
  [Fintype G.V] [Fintype G.E]
  [DecidableEq G.V] [DecidableEq G.E]
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
    x = y := by
  intro x y hx hy hpair
  cases hxy : x = y with
  | refl =>
      rfl
  | _ =>
      exfalso
      exact hxy (by cases hpair; rfl)

theorem block_injective
  (G : Graph)
  [Fintype G.V] [Fintype G.E]
  [DecidableEq G.V] [DecidableEq G.E]
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
    x = y := by
  exact block_injective_bridge G R i v

theorem block_injective
  (G : Graph)
  [Fintype G.V] [Fintype G.E]
  [DecidableEq G.V] [DecidableEq G.E]
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
    x = y := by
  exact block_injective_bridge G R i v

theorem block_injective_unique
  (R i : Nat) (v : G.V)
  {x y : G.V}
  (hx : x ∈ Layer G v i)
  (hy : y ∈ Layer G v i)
  (h :
    (parent G v i x,
     edgeLabel G (parent G v i x) x)
    =
    (parent G v i y,
     edgeLabel G (parent G v i y) y)) :
  x = y :=
by
  exact block_injective G R i v hx hy h
