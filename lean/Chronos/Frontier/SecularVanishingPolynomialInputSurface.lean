namespace Chronos.Frontier

universe u

structure SecularVanishingPolynomial (α : Type u) where
  polynomial : α → Int
  secularVanishes : ∀ x : α, polynomial x = 0

def SecularVanishingPolynomialInputSurface (α : Type u) : Prop :=
  Nonempty (SecularVanishingPolynomial α)

theorem secularVanishingPolynomial_exposes_primitive_vanishing
    {α : Type u}
    (p : SecularVanishingPolynomial α) :
    ∀ x : α, p.polynomial x = 0 :=
  p.secularVanishes

def secularVanishingPolynomialBoundary : String :=
  "BOUNDARY := secular vanishing polynomial is primitive input structure; not antisymmetry, not involution, not cancellation"

end Chronos.Frontier
