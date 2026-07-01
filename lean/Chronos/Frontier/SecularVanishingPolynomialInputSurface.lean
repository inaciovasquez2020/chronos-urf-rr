namespace Chronos.Frontier

universe u

structure SecularVanishingPolynomial (α : Type u) where
  polynomial : α → Int
  secularVanishes : ∀ x : α, polynomial x = 0

def SecularVanishingPolynomialInputSurface (α : Type u) : Prop :=
  Nonempty (SecularVanishingPolynomial α)

structure FormalSecularVanishingPolynomial (σ : Type u) (α : Type v) where
  polynomial : σ
  eval : σ → α → Int
  secularVanishes : ∀ x : α, eval polynomial x = 0
  nontrivial : Prop
  nontrivialWitness : nontrivial

structure NonzeroFormalSecularVanishingPolynomial (σ : Type u) (α : Type v) where
  polynomial : σ
  zeroPolynomial : σ
  eval : σ → α → Int
  secularVanishes : ∀ x : α, eval polynomial x = 0
  syntacticallyNonzero : polynomial ≠ zeroPolynomial

structure SecularVanishingPolynomialSource (α : Type u) where
  polynomial : α → Int
  sourceForcesSecularVanishes : ∀ x : α, polynomial x = 0

def SecularVanishingPolynomialSourceSurface (α : Type u) : Prop :=
  Nonempty (SecularVanishingPolynomialSource α)

theorem secularVanishingPolynomialSource_to_inputSurface
    {α : Type u}
    (s : SecularVanishingPolynomialSource α) :
    SecularVanishingPolynomialInputSurface α :=
  ⟨{
    polynomial := s.polynomial
    secularVanishes := s.sourceForcesSecularVanishes
  }⟩

theorem secularVanishingPolynomialInputSurface_zeroWitness
    (α : Type u) :
    SecularVanishingPolynomialInputSurface α :=
  ⟨{
    polynomial := fun _ => 0
    secularVanishes := by
      intro x
      rfl
  }⟩

theorem secularVanishingPolynomial_exposes_primitive_vanishing
    {α : Type u}
    (p : SecularVanishingPolynomial α) :
    ∀ x : α, p.polynomial x = 0 :=
  p.secularVanishes

def secularVanishingPolynomialBoundary : String :=
  "BOUNDARY := secular vanishing polynomial is primitive input structure; not antisymmetry, not involution, not cancellation"

end Chronos.Frontier
