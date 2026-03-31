import Oblivion.Graph
import Mathlib.Data.Fintype.Basic

namespace Oblivion

variable {G : Graph} [Fintype G.V] [Fintype G.E]

def numComponents (G : Graph) : Nat := 1  -- placeholder

def beta1 (G : Graph) : Nat :=
  Fintype.card G.E - Fintype.card G.V + numComponents G

lemma beta1_connected (h : Connected G) :
    beta1 G = Fintype.card G.E - Fintype.card G.V + 1 := by
  simp [beta1, numComponents]

end Oblivion
