import Cyclone.SSKzIntegration

namespace Chronos

def invariant (G : Cyclone.Graph) : Nat := Cyclone.I G

theorem cyclone_to_chronos (k R : Nat) :
  ∃ Gp Gn,
    Cyclone.FO_equiv k R Gp Gn ∧
    invariant Gp ≠ invariant Gn := by
  obtain ⟨d, h⟩ := Cyclone.SSKz_integration k R
  have h' := h 1 (Nat.succ_le_succ Nat.zero_le)
  rcases h' with ⟨_,_,_,_,hFO,hI⟩
  exact ⟨_,_,hFO,hI⟩

end Chronos
