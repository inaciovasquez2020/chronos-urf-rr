import Chronos.Frontier.ExternalQKDiniCoefficientExtractionRule
import Mathlib

namespace Chronos
namespace Frontier

noncomputable def qPochhammerReal
    (q : ℝ) (r : Nat) (n : Nat) : ℝ :=
  (Finset.range n).prod (fun j => 1 - q ^ (r + j))

noncomputable def externalQKDiniNumerator
    (a c : ℝ) (n : Nat) : ℝ :=
  (-c) ^ n * (a + (2 : ℝ) * (n : ℝ))

noncomputable def externalQKDiniDenominator
    (a q : ℝ) (k n : Nat) : ℝ :=
  a * (4 : ℝ) ^ n
    * qPochhammerReal q 1 n
    * qPochhammerReal (q ^ k) 1 n

noncomputable def externalQKDiniCoefficient
    (a c q : ℝ) (k n : Nat) : ℝ :=
  externalQKDiniNumerator a c n
    / externalQKDiniDenominator a q k n

structure ParameterRestrictedExternalQKDiniCoefficientSlice where
  a : ℝ
  c : ℝ
  q : ℝ
  k : Nat
  B : ℝ
  a_ne_zero : a ≠ 0
  q_pos : 0 < q
  q_lt_one : q < 1
  k_pos : 0 < k
  B_nonneg : 0 ≤ B
  denominator_nonzero :
    ∀ n : Nat, externalQKDiniDenominator a q k n ≠ 0
  coefficient_abs_bound :
    ∀ n : Nat, |externalQKDiniCoefficient a c q k n| ≤ B

theorem externalQKDiniCoefficient_zero_eq_one
    (a c q : ℝ) (k : Nat) (ha : a ≠ 0) :
    externalQKDiniCoefficient a c q k 0 = 1 := by
  simp [
    externalQKDiniCoefficient,
    externalQKDiniNumerator,
    externalQKDiniDenominator,
    qPochhammerReal,
    ha
  ]

theorem parameterRestrictedExternalQKDiniCoefficient_nonzero_witness
    (S : ParameterRestrictedExternalQKDiniCoefficientSlice) :
    ∃ n : Nat,
      externalQKDiniCoefficient S.a S.c S.q S.k n ≠ 0 := by
  refine ⟨0, ?_⟩
  rw [externalQKDiniCoefficient_zero_eq_one S.a S.c S.q S.k S.a_ne_zero]
  norm_num

theorem parameterRestrictedExternalQKDiniCoefficient_denominator_nonzero
    (S : ParameterRestrictedExternalQKDiniCoefficientSlice) :
    ∀ n : Nat,
      externalQKDiniDenominator S.a S.q S.k n ≠ 0 :=
  S.denominator_nonzero

theorem parameterRestrictedExternalQKDiniCoefficientBoundTheorem
    (S : ParameterRestrictedExternalQKDiniCoefficientSlice) :
    ∀ n : Nat,
      |externalQKDiniCoefficient S.a S.c S.q S.k n| ≤ S.B :=
  S.coefficient_abs_bound

def ParameterRestrictedExternalQKDiniCoefficientBoundStatus : String :=
  "CONDITIONAL_PARAMETER_RESTRICTED_BOUND_THEOREM_ONLY"

end Frontier
end Chronos
