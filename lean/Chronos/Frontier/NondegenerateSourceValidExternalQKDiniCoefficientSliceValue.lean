import Chronos.Frontier.ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue
import Mathlib

namespace Chronos.Frontier

structure NondegenerateSourceValidExternalQKDiniCoefficientSlice where
  source_id : String
  a : ℚ
  b : ℚ
  nu : ℚ
  c : ℚ
  q : ℚ
  k : ℚ
  a_pos : 0 < a
  c_nonzero : c ≠ 0
  abs_c_lt_four : |c| < 4
  q_pos : 0 < q
  q_lt_one : q < 1
  k_relation : k = nu + (b + 1) / 2
  k_not_forbidden_zero : k ≠ 0
  denominator_nonzero :
    4 * (1 - q) * (1 - q ^ 1) - |c| ≠ 0
  theorem1_coefficient_condition :
    16 * a * (1 - q) ^ 2 * (1 - q ^ 1) ^ 2 + 2 * a * |c| ^ 2 >
      4 * (3 * a + 2) * |c| * (1 - q) * (1 - q ^ 1)
  theorem2_first_coefficient_condition :
    32 * (a + 2) * |c| * (1 - q) ^ 2 * (1 - q ^ 1) ^ 2 + a * |c| ^ 3 >
      4 * (3 * a + 2) * |c| ^ 2 * (1 - q) * (1 - q ^ 1)
  theorem2_second_coefficient_condition :
    32 * a * (1 - q) ^ 3 * (1 - q ^ 1) ^ 3 +
        4 * (3 * a + 1) * |c| ^ 2 * (1 - q) * (1 - q ^ 1) >
      8 * (5 * a + 4) * |c| * (1 - q) ^ 2 * (1 - q ^ 1) ^ 2 +
        a * |c| ^ 3

def NondegenerateSourceValidExternalQKDiniCoefficientSliceValue :
    NondegenerateSourceValidExternalQKDiniCoefficientSlice where
  source_id := "DOI:10.1155/2022/8496249"
  a := 1
  b := 1
  nu := 0
  c := 1 / 16
  q := 1 / 2
  k := 1
  a_pos := by norm_num
  c_nonzero := by norm_num
  abs_c_lt_four := by norm_num
  q_pos := by norm_num
  q_lt_one := by norm_num
  k_relation := by norm_num
  k_not_forbidden_zero := by norm_num
  denominator_nonzero := by norm_num
  theorem1_coefficient_condition := by norm_num
  theorem2_first_coefficient_condition := by norm_num
  theorem2_second_coefficient_condition := by norm_num

inductive NondegenerateSourceValidExternalQKDiniCoefficientSliceStatus where
  | sliceValueOnlyNoAnalyticDiniEstimateClosure

def nondegenerateSourceValidExternalQKDiniCoefficientSliceStatus :
    NondegenerateSourceValidExternalQKDiniCoefficientSliceStatus :=
  NondegenerateSourceValidExternalQKDiniCoefficientSliceStatus.sliceValueOnlyNoAnalyticDiniEstimateClosure

theorem nondegenerateSourceValidExternalQKDiniCoefficientSliceStatus_eq :
    nondegenerateSourceValidExternalQKDiniCoefficientSliceStatus =
      NondegenerateSourceValidExternalQKDiniCoefficientSliceStatus.sliceValueOnlyNoAnalyticDiniEstimateClosure := rfl

theorem nondegenerateSourceValidExternalQKDiniCoefficientSlice_c_nonzero :
    NondegenerateSourceValidExternalQKDiniCoefficientSliceValue.c ≠ 0 :=
  NondegenerateSourceValidExternalQKDiniCoefficientSliceValue.c_nonzero

end Chronos.Frontier
