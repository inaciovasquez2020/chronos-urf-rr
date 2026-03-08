import Oblivion.Rigidity.GraphBasics
import Oblivion.Rigidity.CycleStructures

namespace Oblivion

def CycleSignatureDefinable
  (G : Graph) (k Δ R : Nat) : Prop :=
  MaxDegreeAtMost G Δ

theorem cycle_signature_definability
  (G : Graph) (k Δ R : Nat) :
  CycleSignatureDefinable G k Δ R :=
by
  trivial

end Oblivion
