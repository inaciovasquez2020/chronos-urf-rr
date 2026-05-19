import Chronos.Frontier.FiniteRationalSinkQuadraticRelaxationTheorem
import Mathlib

namespace Chronos
namespace Frontier

namespace FiniteOrderedRingSinkQuadraticRelaxationTheorem

universe u

structure QuadraticSinkOrderData (α : Type u) where
  zero : α
  mul : α → α → α
  le : α → α → Prop
  zero_square_zero : mul zero zero = zero
  square_nonnegative : ∀ x : α, le zero (mul x x)

def orderedRingSinkRelax
    {α : Type u}
    (D : QuadraticSinkOrderData α)
    (_x : α) : α :=
  D.zero

def orderedRingQuadraticEntropy
    {α : Type u}
    (D : QuadraticSinkOrderData α)
    (x : α) : α :=
  D.mul x x

def orderedRingClosedUnderSinkRelaxation
    {α : Type u}
    (D : QuadraticSinkOrderData α)
    (S : Finset α) : Prop :=
  ∀ x, x ∈ S → orderedRingSinkRelax D x ∈ S

def orderedRingEntropyProductionOn
    {α : Type u}
    (D : QuadraticSinkOrderData α)
    (S : Finset α) : Prop :=
  ∀ x, x ∈ S →
    D.le
      (orderedRingQuadraticEntropy D (orderedRingSinkRelax D x))
      (orderedRingQuadraticEntropy D x)

def orderedRingEntropyMonotoneOn
    {α : Type u}
    (D : QuadraticSinkOrderData α)
    (S : Finset α) : Prop :=
  ∀ x, x ∈ S →
    D.le
      (orderedRingQuadraticEntropy D (orderedRingSinkRelax D x))
      (orderedRingQuadraticEntropy D x)

structure FiniteOrderedRingSinkQuadraticRelaxationCertificate
    {α : Type u}
    (D : QuadraticSinkOrderData α)
    (S : Finset α) : Prop where
  closed_under_relaxation : orderedRingClosedUnderSinkRelaxation D S
  entropy_production : orderedRingEntropyProductionOn D S
  entropy_monotonicity : orderedRingEntropyMonotoneOn D S

theorem ordered_ring_quadratic_entropy_monotone_to_sink
    {α : Type u}
    (D : QuadraticSinkOrderData α)
    (x : α) :
    D.le
      (orderedRingQuadraticEntropy D (orderedRingSinkRelax D x))
      (orderedRingQuadraticEntropy D x) := by
  unfold orderedRingQuadraticEntropy orderedRingSinkRelax
  rw [D.zero_square_zero]
  exact D.square_nonnegative x

theorem ordered_ring_quadratic_entropy_production_nonnegative
    {α : Type u}
    (D : QuadraticSinkOrderData α)
    (x : α) :
    D.le
      (orderedRingQuadraticEntropy D (orderedRingSinkRelax D x))
      (orderedRingQuadraticEntropy D x) := by
  exact ordered_ring_quadratic_entropy_monotone_to_sink D x

theorem finite_ordered_ring_sink_quadratic_relaxation_certificate
    {α : Type u}
    (D : QuadraticSinkOrderData α)
    {S : Finset α}
    (h0 : D.zero ∈ S) :
    FiniteOrderedRingSinkQuadraticRelaxationCertificate D S := by
  refine ⟨?_, ?_, ?_⟩
  · intro x hx
    simpa [orderedRingSinkRelax] using h0
  · intro x hx
    exact ordered_ring_quadratic_entropy_production_nonnegative D x
  · intro x hx
    exact ordered_ring_quadratic_entropy_monotone_to_sink D x

def intQuadraticSinkOrderData : QuadraticSinkOrderData Int where
  zero := 0
  mul := fun x y => x * y
  le := fun x y => x ≤ y
  zero_square_zero := by simp
  square_nonnegative := by
    intro x
    exact mul_self_nonneg x

def ratQuadraticSinkOrderData : QuadraticSinkOrderData Rat where
  zero := 0
  mul := fun x y => x * y
  le := fun x y => x ≤ y
  zero_square_zero := by simp
  square_nonnegative := by
    intro x
    exact mul_self_nonneg x

theorem finite_ordered_ring_sink_quadratic_relaxation_certificate_int
    {S : Finset Int}
    (h0 : (0 : Int) ∈ S) :
    FiniteOrderedRingSinkQuadraticRelaxationCertificate intQuadraticSinkOrderData S := by
  exact finite_ordered_ring_sink_quadratic_relaxation_certificate
    intQuadraticSinkOrderData h0

theorem finite_ordered_ring_sink_quadratic_relaxation_certificate_rat
    {S : Finset Rat}
    (h0 : (0 : Rat) ∈ S) :
    FiniteOrderedRingSinkQuadraticRelaxationCertificate ratQuadraticSinkOrderData S := by
  exact finite_ordered_ring_sink_quadratic_relaxation_certificate
    ratQuadraticSinkOrderData h0

end FiniteOrderedRingSinkQuadraticRelaxationTheorem

end Frontier
end Chronos
