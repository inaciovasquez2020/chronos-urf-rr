import Mathlib.Logic.Function.Basic

namespace Chronos.Frontier

universe u

/--
Known closed theorem demo: Cantor's theorem.

This is a closed benchmark object for the boundary toolkit. It proves only the
standard Cantor non-surjectivity theorem and does not discharge any frontier
claim about complexity theory, gravity, cosmology, Chronos-RR, or foundations
of physics.
-/
theorem known_closed_cantor_boundary_demo
    (α : Type u) :
    ∀ f : α → Set α, ¬ Function.Surjective f := by
  intro f
  exact Function.cantor_surjective f

end Chronos.Frontier
