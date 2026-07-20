import Mathlib.LinearAlgebra.Finsupp.LinearCombination
import Chronos.Frontier.R2Geometry.R2LinearChainComplexGeometry

/-!
# Incidence-derived linear boundary extension

This module reduces construction of the full linear R2 chain complex to
basis-level incidence data.

A two-face is assigned its one-chain boundary, and a one-face is assigned its
zero-chain boundary. `Finsupp.linearCombination` extends both assignments to
`F2`-linear maps.

The global chain-complex identity is derived from the facewise law that the
boundary of every basis two-face is a cycle. It is not supplied separately as
an equality of full linear maps.
-/

noncomputable section

namespace Chronos
namespace Frontier

/--
Basis-level incidence data for an R2 chain complex.

`faceBoundary` and `edgeBoundary` are primitive incidence assignments.

`face_boundary_cycle` is the local parity law from which the global identity

`boundary1 ∘ boundary2 = 0`

is derived.
-/
structure R2IncidenceBoundaryData where
  geometry : R2FillingGeometry

  Face0 : Type
  face0DecidableEq : DecidableEq Face0

  faceBoundary :
    geometry.Face2 →
      geometry.Face1 →₀ F2

  edgeBoundary :
    geometry.Face1 →
      Face0 →₀ F2

  geometry_boundary_eq :
    ∀ filling,
      geometry.boundary2 filling =
        Finsupp.linearCombination
          F2
          faceBoundary
          filling

  face_boundary_cycle :
    ∀ face,
      Finsupp.linearCombination
          F2
          edgeBoundary
          (faceBoundary face) =
        0

attribute [instance]
  R2IncidenceBoundaryData.face0DecidableEq

namespace R2IncidenceBoundaryData

/--
The second boundary map obtained by linearly extending the boundary assigned
to each basis two-face.
-/
def boundary2Linear
    (K : R2IncidenceBoundaryData) :
    (K.geometry.Face2 →₀ F2) →ₗ[F2]
      (K.geometry.Face1 →₀ F2) :=
  Finsupp.linearCombination
    F2
    K.faceBoundary

/--
The first boundary map obtained by linearly extending the boundary assigned
to each basis one-face.
-/
def boundary1Linear
    (K : R2IncidenceBoundaryData) :
    (K.geometry.Face1 →₀ F2) →ₗ[F2]
      (K.Face0 →₀ F2) :=
  Finsupp.linearCombination
    F2
    K.edgeBoundary

/--
The global chain-complex identity follows from the facewise cycle law.
-/
theorem boundary_squared_zero
    (K : R2IncidenceBoundaryData) :
    K.boundary1Linear.comp K.boundary2Linear = 0 := by
  apply Finsupp.lhom_ext
  intro face coefficient

  simp [
    boundary1Linear,
    boundary2Linear,
    K.face_boundary_cycle face
  ]

/--
Basis-level incidence data induces the linear R2 chain-complex carrier.
-/
def toLinearChainComplexGeometry
    (K : R2IncidenceBoundaryData) :
    R2LinearChainComplexGeometry where
  geometry := K.geometry
  Face0 := K.Face0
  face0DecidableEq := K.face0DecidableEq
  boundary2Linear := K.boundary2Linear
  boundary1Linear := K.boundary1Linear

  boundary2_eq := by
    intro filling
    symm
    exact K.geometry_boundary_eq filling

  boundary_squared_zero :=
    K.boundary_squared_zero

/--
Every chain fillable in an incidence-derived R2 chain complex is a cycle.
-/
theorem fillable_isCycle
    (K : R2IncidenceBoundaryData)
    (Adm :
      (K.geometry.Face2 →₀ F2) → Prop)
    (chain :
      K.geometry.Face1 →₀ F2)
    (hFillable :
      K.geometry.Fillable Adm chain) :
    K.toLinearChainComplexGeometry
      |>.toChainComplexGeometry
      |>.IsCycle chain :=
  R2LinearChainComplexGeometry.fillable_isCycle
    K.toLinearChainComplexGeometry
    Adm
    chain
    hFillable

end R2IncidenceBoundaryData

end Frontier
end Chronos
