import Mathlib

namespace Chronos

universe v

variable {E : Type v}

theorem unique_on_tail
  (x : E) (xs : List E) (P : E → Prop) (e : E)
  (h : ∀ y, y ∈ x :: xs → P y → y = e) :
  ∀ y, y ∈ xs → P y → y = e := by
  intro y hy hPy
  exact h y (by simp [hy]) hPy

end Chronos
