import Mathlib

namespace Chronos

theorem neq_eq_not_eq (b t : Bool) :
  (b ≠ t) = (b = !t) := by
  cases b <;> cases t <;> decide

end Chronos
