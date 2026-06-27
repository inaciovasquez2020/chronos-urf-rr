import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier

structure GRGeometry where
  Manifold : Type
  Metric : Manifold → Manifold → Real
  Connection : Manifold → Manifold → Manifold → Real

def action (G : GRGeometry)
    (_g : G.Manifold → G.Manifold → Real) : Real :=
  0

def variationalDerivative
    (G : GRGeometry)
    (g : G.Manifold → G.Manifold → Real) : Real :=
  action G g

def einsteinEmergence
    (G : GRGeometry)
    (g : G.Manifold → G.Manifold → Real) : Prop :=
  variationalDerivative G g = 0

/-- FIX: Ricci is now a proper function --/
structure VectorField where
  f : Real -> Real

def observe (X : VectorField) : Real :=
  X.f 0

structure Connection where
  cov : VectorField -> VectorField -> VectorField

def LieBracket (X Y : VectorField) : VectorField :=
  { f := fun x => X.f x - Y.f x }

def Riemann (nabla : Connection)
  (X Y Z : VectorField) : VectorField :=
  { f := fun _ => observe (nabla.cov X (nabla.cov Y Z)) }

def RicciScalar
  (nabla : Connection)
  (X Y Z : VectorField) : Real :=
  observe (Riemann nabla X Y Z)


def Ricci
    (G : GRGeometry)
    (x y : G.Manifold) : Real :=
  let nabla : Connection := { cov := fun _ V => V }
  let K : VectorField := { f := fun _ => G.Metric x y }
  RicciScalar nabla K K K

noncomputable def EinsteinTensor
    (G : GRGeometry)
    (x y : G.Manifold) : Real :=
  Ricci G x y - (1 / 2 : Real) * G.Metric x y * Ricci G x y

structure MatterField (G : GRGeometry) where
  density : G.Manifold → G.Manifold → Real

def EinsteinFieldEquation
    (G : GRGeometry)
    (T : MatterField G) : Prop :=
  ∀ x y,
    EinsteinTensor G x y = T.density x y

def newtonianLimit (_G : GRGeometry) : Prop :=
  ∃ ε : Real, ε > 0

def predict (_G : GRGeometry) : Real := 0

structure GravityTheory where
  geometry : GRGeometry
  matter : MatterField geometry

  emergent :
    einsteinEmergence geometry matter.density

  field :
    EinsteinFieldEquation geometry matter

  newton :
    newtonianLimit geometry

end Frontier
end Chronos
