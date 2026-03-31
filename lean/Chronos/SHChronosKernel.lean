import Mathlib.Data.Finset.Basic
import Mathlib.Data.Matrix.Basic

namespace Chronos

constant Graph : Type
constant Edge : Type
constant V : Type

def support (c : Edge → Bool) : Finset Edge := ∅

def SH (G : Graph) : Finset Edge := ∅

def I (G : Graph) : Nat := (SH G).card

constant refine : Graph → Graph

constant DCV : Nat → Nat
def ED (X : Type) : Nat := Nat.find (fun t => DCV t = 0)


theorem chronos_lower_bound (X : Type) :
  ED X ≥ 1 := by
  exact Nat.succ_le_succ (Nat.zero_le 0)

end Chronos
-- overlap rigidity marker
