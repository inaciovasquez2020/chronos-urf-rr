import Mathlib.Tactic

namespace Chronos.RapidityGeometry

theorem invariant_volume_conversion
    (a T b p c s k : ℝ)
    (ha : 0 < a)
    (hT : 0 < T)
    (hp : 0 < p)
    (hs : 0 < s)
    (hunit : c^2 - s^2 = 1)
    (hdot : T^2 - b^2 + a^2 = p*c)
    (hmean : T^2 - b^2 - a^2 = p*k)
    (hprod : p^2 =
      (T^2-(b-a)^2)*(T^2-(b+a)^2)) :
    2*a*T = p*s ∧
    (T-a)^2-b^2 = p*(c-s) ∧
    ((T+2*a)/T)*((T-a)^2-b^2)^2 =
      p^2*(c-s)^2*(1+2*(c-k)/s) := by
  have hcs : c^2-1 = s^2 := by
    linarith only [hunit]
  have hsq : (2*a*T)^2 = (p*s)^2 := by
    calc
      (2*a*T)^2 =
          (T^2-b^2+a^2)^2 -
          (T^2-(b-a)^2)*(T^2-(b+a)^2) := by
            ring
      _ = (p*c)^2-p^2 := by
        rw [hdot, ← hprod]
      _ = p^2*(c^2-1) := by ring
      _ = p^2*s^2 := by rw [hcs]
      _ = (p*s)^2 := by ring
  have hST : 2*a*T = p*s := by
    have hf :
        (2*a*T-p*s)*(2*a*T+p*s) = 0 := by
      calc
        _ = (2*a*T)^2-(p*s)^2 := by ring
        _ = 0 := by rw [hsq]; ring
    rcases mul_eq_zero.mp hf with h | h
    · linarith
    · have hh : 0 < 2*a*T+p*s := by positivity
      exact (ne_of_gt hh h).elim
  have hAC : 2*a^2 = p*(c-k) := by
    nlinarith only [hdot,hmean]
  have hbase : (T-a)^2-b^2 = p*(c-s) := by
    nlinarith only [hdot,hST]
  have hzero :
      p*(2*a*s-2*(c-k)*T) = 0 := by
    calc
      _ = 2*a*(p*s)-2*T*(p*(c-k)) := by ring
      _ = 0 := by rw [← hST, ← hAC]; ring
  have hcancel : 2*a*s-2*(c-k)*T = 0 :=
    (mul_eq_zero.mp hzero).resolve_left (ne_of_gt hp)
  have hr : 2*a/T = 2*(c-k)/s := by
    apply (div_eq_div_iff (ne_of_gt hT) (ne_of_gt hs)).2
    linarith only [hcancel]
  refine ⟨hST,hbase,?_⟩
  rw [add_div, div_self (ne_of_gt hT), hr, hbase]
  ring

#print axioms invariant_volume_conversion

end Chronos.RapidityGeometry
