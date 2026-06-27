import Mathlib

namespace Chronos
namespace Frontier

structure GravityEinsteinTheory where
  Manifold : Type
  Matter : Type

  Metric : Manifold → Manifold → Real

  action : (Manifold → Manifold → Real) → Matter → Real

def metricVariation
    {M : Type}
    (g : M → M → Real)
    (h : Real → Real) :
    M → M → Real :=
  fun x y => h (g x y)

def stationaryCondition
    (T : GravityEinsteinTheory)
    (g : T.Manifold → T.Manifold → Real)
    (m : T.Matter) : Prop :=
  ∀ (_δg : T.Manifold → T.Manifold → Real),
    T.action g m ≤ T.action (metricVariation g (fun r => r)) m

def newtonianLimit
    (_T : GravityEinsteinTheory)
    (_g : _T.Manifold → _T.Manifold → Real) : Prop :=
  True

def predict
    (T : GravityEinsteinTheory)
    (g : T.Manifold → T.Manifold → Real)
    (m : T.Matter) : Real :=
  T.action g m

structure GravityScience where
  theory : GravityEinsteinTheory
  metric : theory.Manifold → theory.Manifold → Real
  matter : theory.Matter

  einstein_like :
    stationaryCondition theory metric matter

  newton_limit :
    newtonianLimit theory metric

  predictive :
    Real

end Frontier
end Chronos
