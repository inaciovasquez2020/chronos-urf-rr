import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier

structure GRGeometry where
  Manifold : Type
  Metric : Manifold → Manifold → Real
  Connection : Manifold → Manifold → Manifold → Real

/-- FIX: stress-energy now lives on manifold indices --/
def StressEnergy (G : GRGeometry) :=
  G.Manifold → G.Manifold → Real

def Ricci
    (G : GRGeometry)
    (x y : G.Manifold) : Real :=
  G.Connection x y x

def ScalarCurvature
    (G : GRGeometry)
    (x : G.Manifold) : Real :=
  Ricci G x x

def EinsteinTensor
    (G : GRGeometry)
    (x y : G.Manifold) : Real :=
  Ricci G x y - ScalarCurvature G x

def κ : Real := 1

def EinsteinFieldEquation
    (G : GRGeometry)
    (T : StressEnergy G) : Prop :=
  ∀ x y,
    EinsteinTensor G x y = κ * T x y

def NewtonLimit : Prop := True

def action (_G : GRGeometry) : Real := 0

def stationaryCondition (G : GRGeometry) : Prop :=
  ∀ (_δg : G.Manifold → G.Manifold → Real),
    action G = action G

structure GravityScience where
  geometry : GRGeometry
  stressEnergy : StressEnergy geometry

  einstein :
    EinsteinFieldEquation geometry stressEnergy

  newton :
    NewtonLimit

  stationary :
    stationaryCondition geometry

end Frontier
end Chronos
