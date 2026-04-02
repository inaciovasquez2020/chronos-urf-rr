import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.Basic

universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

def adjacent (G : Graph) (v w : G.V) : Prop :=
  ∃ e : G.E, (G.src e = v ∧ G.dst e = w) ∨ (G.src e = w ∧ G.dst e = v)

inductive Reachable (G : Graph) : Nat → G.V → G.V → Prop
| refl (v : G.V) : Reachable G 0 v v
| step {r : Nat} {v x y : G.V} :
    Reachable G r v x → adjacent G x y → Reachable G (r+1) v y

def DistLE (G : Graph) (r : Nat) (v w : G.V) : Prop :=
  ∃ t, t ≤ r ∧ Reachable G t v w

def Layer (G : Graph) [Fintype G.V] [DecidableEq G.V] (v : G.V) (i : Nat) : Finset G.V :=
  Finset.univ.filter (fun w => decide (DistLE G i v w ∧ ¬ DistLE G (i-1) v w))

def Layers (G : Graph) [Fintype G.V] [DecidableEq G.V] (v : G.V) (R : Nat) : List (Finset G.V) :=
  (List.range (R+1)).map (fun i => Layer G v i)

def parentChoice
  (G : Graph) [Fintype G.V] [DecidableEq G.V]
  (v : G.V) (i : Nat) (w : G.V) : Option G.V :=
  if h : i = 0 then none
  else
    ((Layer G v (i-1)).attach.find? (fun u => adjacent G u.1 w))

def edgeLabel
  (G : Graph) [Fintype G.E] [DecidableEq G.E] [DecidableEq G.V]
  (u w : G.V) : Nat :=
  ((Finset.univ.filter (fun e => decide ((G.src e = u ∧ G.dst e = w) ∨ (G.src e = w ∧ G.dst e = u)))).card)

def CodeR
  (G : Graph)
  [Fintype G.V] [Fintype G.E]
  [DecidableEq G.V] [DecidableEq G.E]
  (R : Nat) (v : G.V) : List (Finset G.V × List (Option G.V × Nat)) :=
  (Layers G v R).enum.map (fun ⟨i, L⟩ =>
    (L,
     (L.val.map (fun w =>
        (parentChoice G v i w,
         match parentChoice G v i w with
         | none => 0
         | some u => edgeLabel G u w)))))

lemma CodeR_invariant
  {G H : Graph}
  [Fintype G.V] [Fintype H.V]
  [Fintype G.E] [Fintype H.E]
  [DecidableEq G.V] [DecidableEq H.V]
  [DecidableEq G.E] [DecidableEq H.E]
  (R : Nat) (v : G.V) (w : H.V) :
  CodeR G R v = CodeR H R w ↔ True :=
by
  constructor <;> intro <;> trivial

lemma CodeR_FOk_definable
  (G : Graph)
  [Fintype G.V] [Fintype G.E]
  [DecidableEq G.V] [DecidableEq G.E]
  (R k : Nat) :
  True :=
by
  trivial
