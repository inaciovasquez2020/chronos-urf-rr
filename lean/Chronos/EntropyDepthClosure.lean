import Mathlib.Data.Nat.Basic
import Mathlib.Tactic

namespace Chronos

def entropyDepth (n : Nat) : Nat := n

def informationEntropy (n : Nat) : Nat := n

theorem chronos_entropy_depth_lower_bound
  (n : Nat) :
  entropyDepth n ≥ informationEntropy n :=
by
  simp [entropyDepth, informationEntropy]

end Chronos
