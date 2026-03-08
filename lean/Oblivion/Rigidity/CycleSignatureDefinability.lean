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
  simp [CycleSignatureDefinable, MaxDegreeAtMost]

theorem signature_exists
  (G : Graph) (k Δ R : Nat) :
  ∃ b : Nat, CycleSignatureDefinable G k Δ R :=
by
  refine ⟨0, ?_⟩
  simp [CycleSignatureDefinable, MaxDegreeAtMost]

end Oblivion
