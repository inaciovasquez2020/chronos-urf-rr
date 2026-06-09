import Chronos.Frontier.ParameterRestrictedExternalQKDiniCoefficientBound

namespace Chronos
namespace Frontier

lemma qPochhammerReal_half_one_pos
    (n : Nat) :
    0 < qPochhammerReal (1 / 2 : ℝ) 1 n := by
  unfold qPochhammerReal
  apply Finset.prod_pos
  intro j _hj
  have hpow_lt :
      (1 / 2 : ℝ) ^ (1 + j) < 1 := by
    exact pow_lt_one₀
      (by norm_num : 0 ≤ (1 / 2 : ℝ))
      (by norm_num : (1 / 2 : ℝ) < 1)
      (by omega : 1 + j ≠ 0)
  nlinarith

noncomputable def ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue :
    ParameterRestrictedExternalQKDiniCoefficientSlice where
  a := 1
  c := 0
  q := (1 / 2 : ℝ)
  k := 1
  B := 1
  a_ne_zero := by norm_num
  q_pos := by norm_num
  q_lt_one := by norm_num
  k_pos := by decide
  B_nonneg := by norm_num
  denominator_nonzero := by
    intro n
    have h4 : (4 : ℝ) ^ n ≠ 0 := pow_ne_zero n (by norm_num)
    have hp : qPochhammerReal (1 / 2 : ℝ) 1 n ≠ 0 :=
      ne_of_gt (qPochhammerReal_half_one_pos n)
    have hden :
        (1 : ℝ) * (4 : ℝ) ^ n
          * qPochhammerReal (1 / 2 : ℝ) 1 n
          * qPochhammerReal (1 / 2 : ℝ) 1 n ≠ 0 :=
      mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) h4) hp) hp
    simpa [externalQKDiniDenominator] using hden
  coefficient_abs_bound := by
    intro n
    cases n with
    | zero =>
        rw [
          externalQKDiniCoefficient_zero_eq_one
            (1 : ℝ) 0 (1 / 2 : ℝ) 1
            (by norm_num)
        ]
        norm_num
    | succ n =>
        simp [
          externalQKDiniCoefficient,
          externalQKDiniNumerator
        ]

theorem concreteParameterRestrictedExternalQKDiniCoefficientSliceValue_nonzero_witness :
    ∃ n : Nat,
      externalQKDiniCoefficient
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.a
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.c
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.q
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.k
        n ≠ 0 :=
  parameterRestrictedExternalQKDiniCoefficient_nonzero_witness
    ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue

theorem concreteParameterRestrictedExternalQKDiniCoefficientSliceValue_denominator_nonzero :
    ∀ n : Nat,
      externalQKDiniDenominator
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.a
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.q
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.k
        n ≠ 0 :=
  parameterRestrictedExternalQKDiniCoefficient_denominator_nonzero
    ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue

theorem concreteParameterRestrictedExternalQKDiniCoefficientSliceValue_bound :
    ∀ n : Nat,
      |externalQKDiniCoefficient
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.a
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.c
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.q
        ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.k
        n|
        ≤ ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.B :=
  parameterRestrictedExternalQKDiniCoefficientBoundTheorem
    ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue

def ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValueStatus : String :=
  "CONCRETE_DEGENERATE_C_ZERO_PARAMETER_SLICE_VALUE_ONLY"

end Frontier
end Chronos
