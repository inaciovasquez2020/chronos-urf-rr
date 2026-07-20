import Chronos.Frontier.R2Geometry.R2MetricFillingGeometry

/-!
# Chain-complex refinement of the genuine R2 geometry

This module refines `R2FillingGeometry` with zero-dimensional faces, a first
boundary operator, additive boundary laws, and the chain-complex identity

`boundary1 (boundary2 F) = 0`.

The metric obstruction kernel only needs the two-to-one boundary operator and
support monotonicity. Concrete Newstein/Heawood geometry must additionally
instantiate this refinement so that filling boundaries are genuine cycles
rather than arbitrary one-chains.
-/

noncomputable section

namespace Chronos
namespace Frontier

/--
A genuine two-dimensional chain-complex refinement of an `R2FillingGeometry`.

The boundary operators are represented extensionally together with their zero
and addition laws. Over `F2`, these laws provide the required linear behavior.
-/
structure R2ChainComplexGeometry where
  geometry : R2FillingGeometry

  Face0 : Type
  face0DecidableEq : DecidableEq Face0

  boundary1 :
    (geometry.Face1 →₀ F2) →
      Face0 →₀ F2

  boundary2_zero :
    geometry.boundary2 0 = 0

  boundary2_add :
    ∀ first second,
      geometry.boundary2 (first + second) =
        geometry.boundary2 first +
          geometry.boundary2 second

  boundary1_zero :
    boundary1 0 = 0

  boundary1_add :
    ∀ first second,
      boundary1 (first + second) =
        boundary1 first +
          boundary1 second

  boundary_squared_zero :
    ∀ filling,
      boundary1 (geometry.boundary2 filling) = 0

attribute [instance]
  R2ChainComplexGeometry.face0DecidableEq

namespace R2ChainComplexGeometry

/--
A one-chain is a cycle when its first boundary vanishes.
-/
def IsCycle
    (K : R2ChainComplexGeometry)
    (chain : K.geometry.Face1 →₀ F2) :
    Prop :=
  K.boundary1 chain = 0

/--
Every boundary of a two-chain is a one-cycle.
-/
theorem boundary2_isCycle
    (K : R2ChainComplexGeometry)
    (filling : K.geometry.Face2 →₀ F2) :
    K.IsCycle (K.geometry.boundary2 filling) :=
  K.boundary_squared_zero filling

/--
Every fillable chain in the underlying metric filling geometry is a cycle in
the chain-complex refinement.
-/
theorem fillable_isCycle
    (K : R2ChainComplexGeometry)
    (Adm : (K.geometry.Face2 →₀ F2) → Prop)
    (chain : K.geometry.Face1 →₀ F2)
    (hFillable : K.geometry.Fillable Adm chain) :
    K.IsCycle chain := by
  rcases hFillable with
    ⟨filling, hBoundary, _hAdmissible⟩

  rw [← hBoundary]

  exact K.boundary2_isCycle filling

end R2ChainComplexGeometry

end Frontier
end Chronos
