import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

namespace Chronos.ECPM.Population

def bern (p : ℝ) : Bool → ℝ
  | true => p
  | false => 1-p

def mass (p : ℝ) : List Bool → ℝ
  | [] => 1
  | b :: h => bern p b * mass p h

noncomputable def mix (p q : ℝ) (h : List Bool) : ℝ :=
  (mass p h + mass q h)/2

noncomputable def total (p q : ℝ) : Nat → List Bool → ℝ
  | 0, h => mix p q h
  | n+1, h =>
      total p q n (true :: h) +
      total p q n (false :: h)

theorem mass_nonneg
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (h : List Bool) :
    0 ≤ mass p h := by
  induction h with
  | nil =>
      exact zero_le_one
  | cons b h ih =>
      cases b with
      | false =>
          exact mul_nonneg (sub_nonneg.mpr hp1) ih
      | true =>
          exact mul_nonneg hp ih

theorem mix_nonneg
    (p q : ℝ)
    (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hq : 0 ≤ q) (hq1 : q ≤ 1)
    (h : List Bool) :
    0 ≤ mix p q h := by
  unfold mix
  exact div_nonneg
    (add_nonneg
      (mass_nonneg p hp hp1 h)
      (mass_nonneg q hq hq1 h))
    (by positivity)

theorem empty_mass (p q : ℝ) :
    mix p q [] = 1 := by
  simp only [mix, mass]
  ring

theorem extension_consistency
    (p q : ℝ) (h : List Bool) :
    mix p q (true :: h) +
      mix p q (false :: h) =
        mix p q h := by
  simp only [mix, mass, bern]
  ring

theorem arbitrary_extension
    (p q : ℝ) (n : Nat) (h : List Bool) :
    total p q n h = mix p q h := by
  induction n generalizing h with
  | zero => rfl
  | succ n ih =>
      simp only [total, ih, extension_consistency]

theorem population_normalized
    (p q : ℝ) (n : Nat) :
    total p q n [] = 1 := by
  rw [arbitrary_extension, empty_mass]

theorem covariance (p d : ℝ) :
    mix p (p+d) [true, true] -
      (mix p (p+d) [true])^2 =
        d^2/4 := by
  simp only [mix, mass, bern]
  ring

theorem not_independent
    (p d : ℝ) (hd : 0 < d) :
    mix p (p+d) [true, true] ≠
      (mix p (p+d) [true])^2 := by
  have hpos :
      0 < mix p (p+d) [true, true] -
        (mix p (p+d) [true])^2 := by
    rw [covariance]
    positivity
  exact ne_of_gt (sub_pos.mp hpos)

#print axioms mass_nonneg
#print axioms mix_nonneg
#print axioms empty_mass
#print axioms extension_consistency
#print axioms arbitrary_extension
#print axioms population_normalized
#print axioms covariance
#print axioms not_independent

end Chronos.ECPM.Population
