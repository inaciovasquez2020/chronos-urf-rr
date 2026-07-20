import Chronos.Frontier.R2Geometry.R2IncidenceBoundaryExtension

/-!
# Vertex-parity construction of the R2 chain-complex law

The preceding incidence extension derives the global identity

`boundary1 ∘ boundary2 = 0`

from a whole-chain statement saying that every basis two-face has zero
one-boundary.

This module reduces that remaining statement to a coordinatewise condition:
for each basis two-face and each vertex, the resulting coefficient at that
vertex is zero in `F2`.

That is the form expected from a concrete parity count on the incidences of
vertices, edges, and faces.
-/

noncomputable section

namespace Chronos
namespace Frontier

/--
Basis incidence data equipped with a vertex-by-vertex parity law.

The full face-boundary cycle equality is derived rather than supplied.
-/
structure R2VertexParityBoundaryData where
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

  vertex_parity :
    ∀ face vertex,
      (Finsupp.linearCombination
          F2
          edgeBoundary
          (faceBoundary face)) vertex =
        0

attribute [instance]
  R2VertexParityBoundaryData.face0DecidableEq

namespace R2VertexParityBoundaryData

/--
The coordinatewise parity law implies that the boundary of each basis
two-face is the zero zero-chain.
-/
theorem face_boundary_cycle
    (K : R2VertexParityBoundaryData)
    (face : K.geometry.Face2) :
    Finsupp.linearCombination
        F2
        K.edgeBoundary
        (K.faceBoundary face) =
      0 := by
  ext vertex
  simpa using K.vertex_parity face vertex

/--
Vertex-parity data induces the incidence-derived boundary carrier.
-/
def toIncidenceBoundaryData
    (K : R2VertexParityBoundaryData) :
    R2IncidenceBoundaryData where
  geometry := K.geometry
  Face0 := K.Face0
  face0DecidableEq := K.face0DecidableEq
  faceBoundary := K.faceBoundary
  edgeBoundary := K.edgeBoundary
  geometry_boundary_eq := K.geometry_boundary_eq
  face_boundary_cycle := K.face_boundary_cycle

/--
The global chain-complex identity is derived from the coordinatewise
vertex-parity law.
-/
theorem boundary_squared_zero
    (K : R2VertexParityBoundaryData) :
    K.toIncidenceBoundaryData.boundary1Linear.comp
        K.toIncidenceBoundaryData.boundary2Linear =
      0 :=
  K.toIncidenceBoundaryData.boundary_squared_zero

/--
Every admissibly fillable chain in a vertex-parity R2 geometry is a cycle.
-/
theorem fillable_isCycle
    (K : R2VertexParityBoundaryData)
    (Adm :
      (K.geometry.Face2 →₀ F2) → Prop)
    (chain :
      K.geometry.Face1 →₀ F2)
    (hFillable :
      K.geometry.Fillable Adm chain) :
    K.toIncidenceBoundaryData
      |>.toLinearChainComplexGeometry
      |>.toChainComplexGeometry
      |>.IsCycle chain :=
  R2IncidenceBoundaryData.fillable_isCycle
    K.toIncidenceBoundaryData
    Adm
    chain
    hFillable

end R2VertexParityBoundaryData

end Frontier
end Chronos
