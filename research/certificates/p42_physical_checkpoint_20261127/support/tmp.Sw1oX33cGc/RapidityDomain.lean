import Mathlib.Tactic

namespace Chronos.RapidityGeometry

theorem rapidity_domain_equiv
    (l m x z e : ℝ) :
    (0 ≤ x ∧ x ≤ l ∧
     0 ≤ z ∧ z ≤ m ∧
     |x-z| ≤ e ∧ e ≤ x+z ∧
     |l-m| < e) ↔
    (|l-m| < e ∧
     |x-z| ≤ e ∧ e ≤ x+z ∧
     x+z+|(x-z)-(l-m)| ≤ l+m) := by
  constructor
  · rintro ⟨hx, hxl, hz, hzm, hd, hs, he⟩
    have hb :
        |(x-z)-(l-m)| ≤ l+m-(x+z) := by
      apply abs_le.mpr
      constructor <;> linarith
    exact ⟨he, hd, hs, by linarith⟩
  · rintro ⟨he, hd, hs, hb⟩
    have ha :
        |(x-z)-(l-m)| ≤ l+m-(x+z) := by
      linarith
    obtain ⟨ha₁, ha₂⟩ := abs_le.mp ha
    have hx : 0 ≤ x := by
      linarith [neg_le_abs (x-z)]
    have hz : 0 ≤ z := by
      linarith [le_abs_self (x-z)]
    exact ⟨hx, by linarith, hz, by linarith,
      hd, hs, he⟩

#print axioms rapidity_domain_equiv

end Chronos.RapidityGeometry
