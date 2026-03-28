import Mathlib.Algebra.BigOperators.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.Parity

open BigOperators

abbrev F2 := ZMod 2

theorem F2_sum_eq_zero_iff_even_support
  {ι : Type*} [DecidableEq ι]
  (s : Finset ι) (f : ι → F2) :
  (∑ i in s, f i = 0) ↔ Even ((s.filter (fun i => f i ≠ 0)).card) := by
  classical
  induction' s using Finset.induction_on with a s ha hs
  · simp
  · by_cases hfa : f a = 0
    · simp [ha, hfa, hs]
    · have hfa1 : f a = 1 := by
        fin_cases f a <;> simp_all [F2]
      rw [Finset.sum_insert ha, hfa1, hs]
      constructor
      · intro h
        have h' : ¬ Even ((s.filter fun i => f i ≠ 0).card) := by
          intro hEven
          have : (1 : F2) + 0 = (0 : F2) := by
            simpa [hEven] using h
          norm_num at this
        have hOdd : Odd ((s.filter fun i => f i ≠ 0).card) := by
          exact Nat.odd_iff_not_even.mpr h'
        simpa [ha, hfa, Nat.odd_iff_not_even] using hOdd
      · intro hEven
        have hOdd : Odd ((s.filter fun i => f i ≠ 0).card) := by
          simpa [ha, hfa] using hEven
        have hs0 : ∑ i in s, f i = 1 := by
          have hsNe : ¬ Even ((s.filter fun i => f i ≠ 0).card) := by
            exact Nat.odd_iff_not_even.mp hOdd
          have : ∑ i in s, f i ≠ 0 := by
            intro hs0
            exact hsNe ((hs.mp hs0))
          fin_cases (∑ i in s, f i) <;> simp_all [F2]
        simpa [hs0]
