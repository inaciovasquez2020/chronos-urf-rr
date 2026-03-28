import Mathlib.Data.Finsupp.Basic
import Mathlib.LinearAlgebra.Basic

abbrev F2 := ZMod 2

variable {m : ℕ}

-- Pairwise support separation condition (disjoint “private” indices)
def hasPrivateIndex (ws : List (Fin m →₀ F2)) : Prop :=
  ∀ w ∈ ws, ∃ i ∈ w.support, ∀ w' ∈ ws, w' ≠ w → i ∉ w'.support

-- Linear independence statement
def linIndep (ws : List (Fin m →₀ F2)) : Prop :=
  ∀ (coeff : ws.length → F2),
    (List.zipWith (fun w c => w • c) ws coeff.toList).foldl (· + ·) 0 = 0 →
    ∀ i, coeff i = 0

-- Axiom: private index ⇒ independence
axiom support_separation_indep
  (ws : List (Fin m →₀ F2)) :
  hasPrivateIndex ws → linIndep ws
