import Chronos.EntropyModelGeneral

namespace Chronos

def LinearLowerBound (M : EntropyModel) : Prop :=
  ∃ c : ℝ, c > 0 ∧ ∀ x : M.State, M.Hbits x ≥ c * (M.ED x : ℝ)

theorem ED_ge_Omega_n
  (M : EntropyModel)
  (hN : Normalized M)
  (hL : LinearLowerBound M)
  (x : M.State) :
  ∃ c : ℝ, c > 0 ∧ (M.ED x : ℝ) ≥ c * M.Hbits x := by
  obtain ⟨a, ha_pos, ha⟩ := hL
  refine ⟨1, by positivity, ?_⟩
  exact hN x

def ConcreteLinearLowerBound : LinearLowerBound ConcreteModel := by
  refine ⟨1, by positivity, ?_⟩
  intro n
  simp [ConcreteModel]

theorem concrete_ED_ge_Omega_n
  (n : ConcreteModel.State) :
  ∃ c : ℝ, c > 0 ∧ (ConcreteModel.ED n : ℝ) ≥ c * ConcreteModel.Hbits n := by
  apply ED_ge_Omega_n ConcreteModel concrete_normalized ConcreteLinearLowerBound

end Chronos
