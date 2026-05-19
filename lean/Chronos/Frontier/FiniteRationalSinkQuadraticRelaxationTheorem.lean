import Chronos.Frontier.FiniteSinkQuadraticRelaxationTheorem
import Mathlib.Data.Finset.Basic
import Mathlib

namespace Chronos
namespace Frontier

namespace FiniteRationalSinkQuadraticRelaxationTheorem

def rationalSinkRelax (_x : Rat) : Rat := 0

def rationalQuadraticEntropy (x : Rat) : Rat :=
  x * x

def rationalClosedUnderSinkRelaxation (S : Finset Rat) : Prop :=
  ∀ x, x ∈ S → rationalSinkRelax x ∈ S

def rationalEntropyProductionOn (S : Finset Rat) : Prop :=
  ∀ x, x ∈ S → rationalQuadraticEntropy (rationalSinkRelax x) ≤ rationalQuadraticEntropy x

def rationalEntropyMonotoneOn (S : Finset Rat) : Prop :=
  ∀ x, x ∈ S → rationalQuadraticEntropy (rationalSinkRelax x) ≤ rationalQuadraticEntropy x

structure FiniteRationalSinkQuadraticRelaxationCertificate (S : Finset Rat) : Prop where
  closed_under_relaxation : rationalClosedUnderSinkRelaxation S
  entropy_production : rationalEntropyProductionOn S
  entropy_monotonicity : rationalEntropyMonotoneOn S

theorem rational_quadratic_entropy_monotone_to_sink (x : Rat) :
    rationalQuadraticEntropy (rationalSinkRelax x) ≤ rationalQuadraticEntropy x := by
  have h : (0 : Rat) ≤ x * x := mul_self_nonneg x
  simpa [rationalQuadraticEntropy, rationalSinkRelax] using h

theorem rational_quadratic_entropy_production_nonnegative (x : Rat) :
    rationalQuadraticEntropy (rationalSinkRelax x) ≤ rationalQuadraticEntropy x := by
  exact rational_quadratic_entropy_monotone_to_sink x

theorem finite_rational_sink_quadratic_relaxation_certificate
    {S : Finset Rat}
    (h0 : (0 : Rat) ∈ S) :
    FiniteRationalSinkQuadraticRelaxationCertificate S := by
  refine ⟨?_, ?_, ?_⟩
  · intro x hx
    simpa [rationalSinkRelax] using h0
  · intro x hx
    exact rational_quadratic_entropy_production_nonnegative x
  · intro x hx
    exact rational_quadratic_entropy_monotone_to_sink x

def concreteRationalSymmetricDomain : Finset Rat :=
  {(-2 : Rat), (-1 : Rat), 0, 1, 2}

theorem concrete_rational_symmetric_domain_certificate :
    FiniteRationalSinkQuadraticRelaxationCertificate concreteRationalSymmetricDomain := by
  exact finite_rational_sink_quadratic_relaxation_certificate (by decide)

end FiniteRationalSinkQuadraticRelaxationTheorem

end Frontier
end Chronos
