namespace Chronos

structure EntropyModel where
  State : Type
  ED : State → Nat
  Hbits : State → ℝ

def Normalized (M : EntropyModel) : Prop :=
  ∀ x : M.State, (M.ED x : ℝ) ≥ M.Hbits x

theorem normalization_lower_bound_general
  (M : EntropyModel)
  (hM : Normalized M)
  (x : M.State)
  (λ : ℝ)
  (hλ : λ ≥ 1) :
  λ * (M.ED x : ℝ) ≥ M.Hbits x := by
  have h1 : λ * (M.ED x : ℝ) ≥ (M.ED x : ℝ) := by
    have hED : (0 : ℝ) ≤ (M.ED x : ℝ) := by exact_mod_cast Nat.zero_le (M.ED x)
    nlinarith
  have h2 : (M.ED x : ℝ) ≥ M.Hbits x := hM x
  nlinarith

def ConcreteModel : EntropyModel where
  State := Nat
  ED := fun n => n
  Hbits := fun n => (n : ℝ)

theorem concrete_normalized : Normalized ConcreteModel := by
  intro n
  simp [ConcreteModel]

end Chronos
