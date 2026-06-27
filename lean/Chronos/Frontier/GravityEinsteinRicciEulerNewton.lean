import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier

structure GRGeometry where
  Manifold : Type
  Metric : Manifold → Manifold → Real

def Ricci
    (M : GRGeometry)
    (g : M.Manifold → M.Manifold → Real) :
    M.Manifold → M.Manifold → Real :=
  fun x y => g x y

def ScalarCurvature
    (M : GRGeometry)
    (_g : M.Manifold → M.Manifold → Real) : Real :=
  0

def EinsteinTensor
    (M : GRGeometry)
    (g : M.Manifold → M.Manifold → Real) :
    M.Manifold → M.Manifold → Real :=
  fun x y =>
    Ricci M g x y - ScalarCurvature M g

structure Matter where
  density : Real

def action
    (M : GRGeometry)
    (_g : M.Manifold → M.Manifold → Real)
    (_m : Matter) : Real :=
  0

def metricVariation
    {M : GRGeometry}
    (g : M.Manifold → M.Manifold → Real)
    (δ : Real → Real) :
    M.Manifold → M.Manifold → Real :=
  fun x y => δ (g x y)

def stationaryCondition
    (M : GRGeometry)
    (g : M.Manifold → M.Manifold → Real)
    (m : Matter) : Prop :=
  ∀ (_δg : M.Manifold → M.Manifold → Real),
    action M g m ≤ action M (metricVariation g (fun r => r)) m

def newtonianLimit
    (_M : GRGeometry)
    (_g : _M.Manifold → _M.Manifold → Real) : Prop :=
  True

def predict
    (M : GRGeometry)
    (g : M.Manifold → M.Manifold → Real)
    (m : Matter) : Real :=
  action M g m

structure GravityScience where
  theory : GRGeometry
  metric : theory.Manifold → theory.Manifold → Real
  matter : Matter

  einstein :
    EinsteinTensor theory metric = 0

  stationary :
    stationaryCondition theory metric matter

  newton :
    newtonianLimit theory metric

  observable :
    Real

end Frontier
end Chronos
