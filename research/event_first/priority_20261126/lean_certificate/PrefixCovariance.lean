import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace Chronos.PrefixAudit

noncomputable def eTwo (s0 v c : ℝ) : ℝ :=
  |s0 + v + c - 1 / 10|

noncomputable def eThree (a s0 s1 s2 v w c : ℝ) : ℝ :=
  (|a - 53 / 70| +
   |s0 + s1 + s2 - 33 / 175| +
   |v - 9 / 350| +
   |w - 9 / 350| +
   |c - 1 / 350|) / 2

noncomputable def eCov (s0 s1 s2 : ℝ) : ℝ :=
  (|s0 - (s0 + s1 + s2) / 3| +
   |s1 - (s0 + s1 + s2) / 3| +
   |s2 - (s0 + s1 + s2) / 3|) / 2

theorem universal_discrepancy (e v w c : ℝ) :
    (e + 2*v + 2*w + 3*c)/3 -
      (e/3 + v + c) = (2*w-v)/3 := by
  ring

theorem sharp_lower
    (a s0 s1 s2 v w c : ℝ)
    (hmass : a + s0 + s1 + s2 + v + w + c = 1) :
    (3 : ℝ)/350 ≤
      eTwo s0 v c +
      eThree a s0 s1 s2 v w c +
      eCov s0 s1 s2 := by
  unfold eTwo eThree eCov
  have h2 := neg_le_abs (s0 + v + c - 1/10)
  have h3 :
      (s0+s1+s2)/3 + v+c-16/175 ≤
      (|a-53/70| +
       |s0+s1+s2-33/175| +
       |v-9/350| +
       |w-9/350| +
       |c-1/350|)/2 := by
    linarith only [
      hmass,
      neg_le_abs (a-53/70),
      neg_le_abs (s0+s1+s2-33/175),
      abs_nonneg (s0+s1+s2-33/175),
      le_abs_self (v-9/350),
      neg_le_abs (w-9/350),
      le_abs_self (c-1/350)]
  have hc :
      s0-(s0+s1+s2)/3 ≤
      (|s0-(s0+s1+s2)/3| +
       |s1-(s0+s1+s2)/3| +
       |s2-(s0+s1+s2)/3|)/2 := by
    linarith only [
      le_abs_self (s0-(s0+s1+s2)/3),
      neg_le_abs (s1-(s0+s1+s2)/3),
      neg_le_abs (s2-(s0+s1+s2)/3)]
  linarith only [h2, h3, hc]

theorem sharp_attainment
    (x y z : ℝ)
    (hx : 0 ≤ x) (hy : 0 ≤ y) (hz : 0 ≤ z)
    (hs : x+y+z = 3/350) :
    0 ≤ 53/70-y ∧
    0 ≤ 11/175+z ∧
    0 ≤ 11/175-z ∧
    (0 : ℝ) ≤ 11/175 ∧
    (0 : ℝ) ≤ 9/350 ∧
    0 ≤ 1/350+y ∧
    (53/70-y)+(11/175+z)+(11/175-z)+
      11/175+9/350+9/350+(1/350+y) = 1 ∧
    eTwo (11/175+z) (9/350) (1/350+y) = x ∧
    eThree (53/70-y) (11/175+z) (11/175-z)
      (11/175) (9/350) (9/350) (1/350+y) = y ∧
    eCov (11/175+z) (11/175-z) (11/175) = z := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · linarith
  · linarith
  · linarith
  · linarith
  · linarith
  · linarith
  · ring
  · unfold eTwo
    have h : (11/175:ℝ)+z+9/350+(1/350+y)-1/10 = -x := by
      linarith
    rw [h, abs_neg, abs_of_nonneg hx]
  · unfold eThree
    have ha : (53/70:ℝ)-y-53/70 = -y := by ring
    have hb : (11/175:ℝ)+z+(11/175-z)+11/175-33/175 = 0 := by
      ring
    have hc : (1/350:ℝ)+y-1/350 = y := by ring
    simp only [ha, hb, hc, sub_self, abs_neg,
      abs_zero, abs_of_nonneg hy]
    ring
  · unfold eCov
    have h0 : (11/175:ℝ)+z -
        ((11/175+z)+(11/175-z)+11/175)/3 = z := by ring
    have h1 : (11/175:ℝ)-z -
        ((11/175+z)+(11/175-z)+11/175)/3 = -z := by ring
    have h2 : (11/175:ℝ) -
        ((11/175+z)+(11/175-z)+11/175)/3 = 0 := by ring
    simp only [h0, h1, h2, abs_neg,
      abs_zero, abs_of_nonneg hz]
    ring

#print axioms universal_discrepancy
#print axioms sharp_lower
#print axioms sharp_attainment

end Chronos.PrefixAudit
