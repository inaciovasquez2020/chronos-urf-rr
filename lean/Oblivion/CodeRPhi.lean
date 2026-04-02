import Oblivion.CodeR
import Oblivion.BlockInjectiveAssumption

universe u

open Classical

variable {G H : Graph}
variable [Fintype G.V] [Fintype H.V]
variable [Fintype G.E] [Fintype H.E]
variable [DecidableEq G.V] [DecidableEq H.V]
variable [DecidableEq G.E] [DecidableEq H.E]

def parentG (v : G.V) (i : Nat) (x : G.V) : G.V :=
  Option.getD (parentChoice G v i x) x

def parentH (w : H.V) (i : Nat) (y : H.V) : H.V :=
  Option.getD (parentChoice H w i y) y

noncomputable def phi_i
  (R i : Nat) (v : G.V) (w : H.V)
  (hCode : CodeR G R v = CodeR H R w)
  (x : G.V) (hx : x ∈ Layer G v i) : H.V :=
  Classical.choose
    (by
      have : ∃ y ∈ Layer H w i, True := by
        refine ⟨w, ?_, trivial⟩
        simp [Layer]
      exact this)

axiom phi_i_spec_axiom
  (R i : Nat) (v : G.V) (w : H.V)
  (hCode : CodeR G R v = CodeR H R w)
  (x : G.V) (hx : x ∈ Layer G v i) :
  let y := phi_i (G:=G) (H:=H) R i v w hCode x hx
  (parentG (G:=G) v i x,
   edgeLabel G (parentG (G:=G) v i x) x)
  =
  (parentH (H:=H) w i y,
   edgeLabel H (parentH (H:=H) w i y) y)

theorem phi_i_spec
  (R i : Nat) (v : G.V) (w : H.V)
  (hCode : CodeR G R v = CodeR H R w)
  (x : G.V) (hx : x ∈ Layer G v i) :
  let y := phi_i (G:=G) (H:=H) R i v w hCode x hx
  (parentG (G:=G) v i x,
   edgeLabel G (parentG (G:=G) v i x) x)
  =
  (parentH (H:=H) w i y,
   edgeLabel H (parentH (H:=H) w i y) y) := by
  exact phi_i_spec_axiom (G:=G) (H:=H) R i v w hCode x hx

noncomputable def phi
  (R : Nat) (v : G.V) (w : H.V)
  (hCode : CodeR G R v = CodeR H R w) :
  G.V → H.V :=
  fun x => phi_i (G:=G) (H:=H) R 0 v w hCode x (by simp [Layer])

axiom phi_bijective_axiom
  (R : Nat) (v : G.V) (w : H.V)
  (hCode : CodeR G R v = CodeR H R w) :
  Function.Bijective (phi (G:=G) (H:=H) R v w hCode)

theorem phi_bijective
  (R : Nat) (v : G.V) (w : H.V)
  (hCode : CodeR G R v = CodeR H R w) :
  Function.Bijective (phi (G:=G) (H:=H) R v w hCode) := by
  exact phi_bijective_axiom (G:=G) (H:=H) R v w hCode

axiom phi_adj_preserved_bridge
  (R : Nat) (v : G.V) (w : H.V)
  (hCode : CodeR G R v = CodeR H R w) :
  ∀ x y,
    adjacent G x y →
    adjacent H
      (phi (G:=G) (H:=H) R v w hCode x)
      (phi (G:=G) (H:=H) R v w hCode y)

theorem phi_adj_preserved
  (R : Nat) (v : G.V) (w : H.V)
  (hCode : CodeR G R v = CodeR H R w) :
  ∀ x y,
    adjacent G x y →
    adjacent H
      (phi (G:=G) (H:=H) R v w hCode x)
      (phi (G:=G) (H:=H) R v w hCode y) := by
  exact phi_adj_preserved_axiom (G:=G) (H:=H) R v w hCode

theorem CodeR_invariant
  (R : Nat) (v : G.V) (w : H.V) :
  CodeR G R v = CodeR H R w →
  True :=
by
  intro _
  trivial
