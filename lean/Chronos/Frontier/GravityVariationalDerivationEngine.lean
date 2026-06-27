import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier

structure GRGeometry where
  Manifold : Type
  Metric : Manifold → Manifold → Real
  Connection : Manifold → Manifold → Manifold → Real

def action (G : GRGeometry)
    (g : G.Manifold → G.Manifold → Real) : Real :=
  0

def metricVariation
    (g : Real → Real)
    (δ : Real → Real) : Real :=
  δ (g 0)

def variationalDerivative
    (G : GRGeometry)
    (g : G.Manifold → G.Manifold → Real) : Real :=
  action G g

def einsteinEmergence
    (G : GRGeometry)
    (g : G.Manifold → G.Manifold → Real) : Prop :=
  variationalDerivative G g = 0

def Ricci (G : GRGeometry) :=
  G.Manifold → G.Manifold → Real

/-- FIX: Einstein tensor is now fully applied function --/
def EinsteinTensor
    (G : GRGeometry)
    (x y : G.Manifold) : Real :=
  0

structure MatterField (G : GRGeometry) where
  density : G.Manifold → G.Manifold → Real

def EinsteinFieldEquation
    (G : GRGeometry)
    (T : MatterField G) : Prop :=
  ∀ x y,
    EinsteinTensor G x y = T.density x y

def newtonianLimit : Prop := True

def predict (G : GRGeometry) : Real := 0

structure GravityTheory where
  geometry : GRGeometry
  matter : MatterField geometry

  emergent :
    einsteinEmergence geometry matter.density

  field :
    EinsteinFieldEquation geometry matter

  newton :
    newtonianLimit

end Frontier
end Chronos
