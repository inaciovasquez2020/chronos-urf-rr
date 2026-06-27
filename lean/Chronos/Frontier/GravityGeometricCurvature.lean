import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier

structure GravityGeometricCurvature where
  Manifold : Type
  Matter : Type

  Metric : Manifold → Manifold → Real
  connection : Manifold → Manifold → Manifold → Real
  curvature : Manifold → Manifold → Real

  action : (Manifold → Manifold → Real) → Matter → Real

def einsteinFieldTarget
    (G : GravityGeometricCurvature)
    : Prop :=
  ∀ (_g : G.Manifold → G.Manifold → Real),
    ∃ (_R : G.Manifold → G.Manifold → Real),
      True

def newtonLimitTarget
    (_G : GravityGeometricCurvature)
    : Prop := True

def predict
    (G : GravityGeometricCurvature)
    (m : G.Matter) : Real :=
  G.action G.Metric m

structure GravityScience where
  theory : GravityGeometricCurvature
  metric : theory.Manifold → theory.Manifold → Real
  matter : theory.Matter

  einstein :
    einsteinFieldTarget theory

  newton :
    newtonLimitTarget theory

  prediction :
    Real

end Frontier
end Chronos
