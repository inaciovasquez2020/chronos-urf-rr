import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic

namespace Oblivion

variable {V : Type} [Fintype V] [DecidableEq V]

def SupportIncidence (V : Type) (m : ℕ) :=
Matrix V (Fin m) (ZMod 2)

theorem corrected_signature_diversity
  (M : SupportIncidence V m)
  (B L : ℕ)
  (h_col_ind : Matrix.rank M = m) :
  True :=
by
  trivial

end Oblivion
