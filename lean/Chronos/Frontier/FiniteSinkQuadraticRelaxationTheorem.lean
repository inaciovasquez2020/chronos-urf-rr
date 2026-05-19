import Chronos.Frontier.TemporalRelaxationChainStatusSnapshot
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Int.Basic

namespace Chronos
namespace Frontier

namespace FiniteSinkQuadraticRelaxationTheorem

def sinkRelax (_x : Int) : Int := 0

def quadraticEntropy (x : Int) : Nat :=
  Int.natAbs x * Int.natAbs x

def closedUnderSinkRelaxation (S : Finset Int) : Prop :=
  ∀ x, x ∈ S → sinkRelax x ∈ S

def entropyProductionOn (S : Finset Int) : Prop :=
  ∀ x, x ∈ S → quadraticEntropy (sinkRelax x) ≤ quadraticEntropy x

def entropyMonotoneOn (S : Finset Int) : Prop :=
  ∀ x, x ∈ S → quadraticEntropy (sinkRelax x) ≤ quadraticEntropy x

structure FiniteSinkQuadraticRelaxationCertificate (S : Finset Int) : Prop where
  closed_under_relaxation : closedUnderSinkRelaxation S
  entropy_production : entropyProductionOn S
  entropy_monotonicity : entropyMonotoneOn S

theorem quadratic_entropy_monotone_to_sink (x : Int) :
    quadraticEntropy (sinkRelax x) ≤ quadraticEntropy x := by
  simp [quadraticEntropy, sinkRelax]

theorem quadratic_entropy_production_nonnegative (x : Int) :
    quadraticEntropy (sinkRelax x) ≤ quadraticEntropy x := by
  exact quadratic_entropy_monotone_to_sink x

theorem finite_sink_quadratic_relaxation_certificate
    {S : Finset Int}
    (h0 : (0 : Int) ∈ S) :
    FiniteSinkQuadraticRelaxationCertificate S := by
  refine ⟨?_, ?_, ?_⟩
  · intro x hx
    simpa [sinkRelax] using h0
  · intro x hx
    exact quadratic_entropy_production_nonnegative x
  · intro x hx
    exact quadratic_entropy_monotone_to_sink x

def concreteSymmetricDomain : Finset Int :=
  {(-2 : Int), (-1 : Int), 0, 1, 2}

theorem concrete_symmetric_domain_certificate :
    FiniteSinkQuadraticRelaxationCertificate concreteSymmetricDomain := by
  exact finite_sink_quadratic_relaxation_certificate (by decide)

end FiniteSinkQuadraticRelaxationTheorem

end Frontier
end Chronos
