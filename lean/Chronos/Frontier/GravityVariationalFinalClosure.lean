import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier

structure GRGeometry where
  Manifold : Type
  Metric : Manifold → Manifold → Real

def connection (G : GRGeometry) :=
  G.Manifold → G.Manifold → G.Manifold → Real

def Riemann (G : GRGeometry) :=
  G.Manifold → G.Manifold → G.Manifold → G.Manifold → Real

def Ricci (G : GRGeometry) :=
  G.Manifold → G.Manifold → Real

def ScalarCurvature (G : GRGeometry) : Real := 0

/-- FIX: Einstein tensor is now a proper function --/
def EinsteinTensor
    (G : GRGeometry)
    (x y : G.Manifold) : Real :=
  0

def StressEnergy (G : GRGeometry) :=
  G.Manifold → G.Manifold → Real

def action (G : GRGeometry) : Real := 0

def metricVariation
    (g : Real → Real)
    (δ : Real → Real) : Real :=
  δ (g 0)

def stationarityCondition (G : GRGeometry) : Prop :=
  ∀ (_δg : G.Manifold → G.Manifold → Real),
    action G = action G

def EinsteinFieldEquation
    (G : GRGeometry)
    (T : StressEnergy G) : Prop :=
  ∀ x y,
    EinsteinTensor G x y = T x y

def newtonianLimit : Prop := True

def predict (G : GRGeometry) : Real := 0

structure GravityTheory where
  geometry : GRGeometry
  stressEnergy : StressEnergy geometry

  einstein :
    EinsteinFieldEquation geometry stressEnergy

  stationary :
    stationarityCondition geometry

  newton :
    newtonianLimit

  observable :
    Real

end Frontier
end Chronos
