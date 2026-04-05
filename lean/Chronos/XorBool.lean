import Mathlib

namespace Chronos

theorem bool_xor_flip
  (b1 b2 t1 t2 : Bool)
  (hb : b1 ≠ b2)
  (ht : t1 = t2) :
  (b1 ≠ t1) ≠ (b2 ≠ t2) := by
  cases b1 <;> cases b2 <;>
  cases t1 <;> cases t2 <;>
  simp at hb ht ⊢

end Chronos
