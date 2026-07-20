import Mathlib.LinearAlgebra.Finsupp.Defs
import Chronos.Frontier.R2Geometry.R2ChainComplexGeometry

/-!
# Linear chain-complex refinement of genuine R2 geometry

This module replaces separately supplied zero and addition laws with actual
`F2`-linear boundary maps.

The second boundary map agrees with the boundary operator in the underlying
metric filling geometry. The chain-complex identity is stated as an equality
of linear maps and transported to `R2ChainComplexGeometry`.

Concrete incidence geometry must still construct these linear maps and prove
that their composition is zero.
-/

noncomputable section

namespace Chronos
namespace Frontier

/--
An `F2`-linear chain-complex refinement of a genuine metric filling geometry.
-/
structure R2LinearChainComplexGeometry where
  geometry : R2FillingGeometry

  Face0 : Type
  face0DecidableEq : DecidableEq Face0

  boundary2Linear :
    (geometry.Face2 →₀ F2) →ₗ[F2]
      (geometry.Face1 →₀ F2)

  boundary1Linear :
    (geometry.Face1 →₀ F2) →ₗ[F2]
      (Face0 →₀ F2)

  boundary2_eq :
    ∀ filling,
      boundary2Linear filling =
        geometry.boundary2 filling

  boundary_squared_zero :
    boundary1Linear.comp boundary2Linear = 0

attribute [instance]
  R2LinearChainComplexGeometry.face0DecidableEq

namespace R2LinearChainComplexGeometry

/--
Forget the explicit linear-map packaging while retaining the induced
chain-complex structure.
-/
def toChainComplexGeometry
    (K : R2LinearChainComplexGeometry) :
    R2ChainComplexGeometry where
  geometry := K.geometry
  Face0 := K.Face0
  face0DecidableEq := K.face0DecidableEq

  boundary1 := fun chain =>
    K.boundary1Linear chain

  boundary2_zero := by
    calc
      K.geometry.boundary2 0
          = K.boundary2Linear 0 := by
              symm
              exact K.boundary2_eq 0
      _ = 0 :=
        K.boundary2Linear.map_zero

  boundary2_add := by
    intro first second

    calc
      K.geometry.boundary2 (first + second)
          = K.boundary2Linear (first + second) := by
              symm
              exact K.boundary2_eq (first + second)
      _ =
          K.boundary2Linear first +
            K.boundary2Linear second :=
        K.boundary2Linear.map_add first second
      _ =
          K.geometry.boundary2 first +
            K.geometry.boundary2 second := by
        rw [
          K.boundary2_eq first,
          K.boundary2_eq second
        ]

  boundary1_zero :=
    K.boundary1Linear.map_zero

  boundary1_add := by
    intro first second
    exact K.boundary1Linear.map_add first second

  boundary_squared_zero := by
    intro filling

    rw [← K.boundary2_eq filling]

    have hComposition :=
      congrArg
        (fun linearMap => linearMap filling)
        K.boundary_squared_zero

    simpa using hComposition

/--
Every fillable chain is a cycle in an `F2`-linear R2 chain complex.
-/
theorem fillable_isCycle
    (K : R2LinearChainComplexGeometry)
    (Adm :
      (K.geometry.Face2 →₀ F2) → Prop)
    (chain :
      K.geometry.Face1 →₀ F2)
    (hFillable :
      K.geometry.Fillable Adm chain) :
    K.toChainComplexGeometry.IsCycle chain :=
  R2ChainComplexGeometry.fillable_isCycle
    K.toChainComplexGeometry
    Adm
    chain
    hFillable

end R2LinearChainComplexGeometry

end Frontier
end Chronos
