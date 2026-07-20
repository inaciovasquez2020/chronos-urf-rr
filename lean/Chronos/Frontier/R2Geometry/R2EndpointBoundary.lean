import Chronos.Frontier.R2Geometry.R2VertexParityBoundary

/-!
# Endpoint-derived R2 edge boundaries

The preceding vertex-parity carrier accepts an arbitrary zero-chain boundary
for every one-face.

This module removes that freedom. Every one-face is given a source and target
vertex, and its boundary is derived as the `F2` sum of those endpoint basis
chains.

The remaining local chain-complex obligation is the concrete endpoint parity
count around each basis two-face.
-/

noncomputable section

namespace Chronos
namespace Frontier

/--
The `F2` zero-chain containing the source and target of an edge.

The decidable-equality instance is passed explicitly so this construction can
also be used inside later structure fields.
-/
def r2EndpointChain
    (Vertex : Type)
    (source target : Vertex) :
    Vertex →₀ F2 :=
  Finsupp.single source (1 : F2) +
    Finsupp.single target (1 : F2)

/--
R2 incidence data in which every edge boundary is derived from its two
endpoints.
-/
structure R2EndpointBoundaryData where
  geometry : R2FillingGeometry

  Face0 : Type
  face0DecidableEq : DecidableEq Face0

  edgeSource :
    geometry.Face1 →
      Face0

  edgeTarget :
    geometry.Face1 →
      Face0

  faceBoundary :
    geometry.Face2 →
      geometry.Face1 →₀ F2

  geometry_boundary_eq :
    ∀ filling,
      geometry.boundary2 filling =
        Finsupp.linearCombination
          F2
          faceBoundary
          filling

  endpoint_parity :
    ∀ face vertex,
      (Finsupp.linearCombination
          F2
          (fun edge =>
            r2EndpointChain
              Face0
              (edgeSource edge)
              (edgeTarget edge))
          (faceBoundary face)) vertex =
        0

attribute [instance]
  R2EndpointBoundaryData.face0DecidableEq

namespace R2EndpointBoundaryData

/--
The zero-chain boundary of an edge is the `F2` sum of its source and target
vertices.
-/
def edgeBoundary
    (K : R2EndpointBoundaryData)
    (edge : K.geometry.Face1) :
    K.Face0 →₀ F2 :=
  r2EndpointChain
    K.Face0
    (K.edgeSource edge)
    (K.edgeTarget edge)

/--
The endpoint-derived boundary has its defining source-plus-target form.
-/
theorem edgeBoundary_eq
    (K : R2EndpointBoundaryData)
    (edge : K.geometry.Face1) :
    K.edgeBoundary edge =
      r2EndpointChain
        K.Face0
        (K.edgeSource edge)
        (K.edgeTarget edge) :=
  rfl

/--
Endpoint incidence data induces the vertex-parity boundary carrier.
-/
def toVertexParityBoundaryData
    (K : R2EndpointBoundaryData) :
    R2VertexParityBoundaryData where
  geometry := K.geometry
  Face0 := K.Face0
  face0DecidableEq := K.face0DecidableEq
  faceBoundary := K.faceBoundary
  edgeBoundary := K.edgeBoundary
  geometry_boundary_eq := K.geometry_boundary_eq

  vertex_parity := by
    intro face vertex

    simpa [edgeBoundary] using
      K.endpoint_parity face vertex

/--
The endpoint parity condition implies the global chain-complex identity.
-/
theorem boundary_squared_zero
    (K : R2EndpointBoundaryData) :
    (K.toVertexParityBoundaryData
        |>.toIncidenceBoundaryData
        |>.boundary1Linear).comp
        (K.toVertexParityBoundaryData
          |>.toIncidenceBoundaryData
          |>.boundary2Linear) =
      0 := by
  simpa using
    (R2VertexParityBoundaryData.boundary_squared_zero
      K.toVertexParityBoundaryData)

/--
Every admissibly fillable chain in endpoint-derived incidence data is a cycle.
-/
theorem fillable_isCycle
    (K : R2EndpointBoundaryData)
    (Adm :
      (K.geometry.Face2 →₀ F2) → Prop)
    (chain :
      K.geometry.Face1 →₀ F2)
    (hFillable :
      K.geometry.Fillable Adm chain) :
    (K.toVertexParityBoundaryData
        |>.toIncidenceBoundaryData
        |>.toLinearChainComplexGeometry
        |>.toChainComplexGeometry).IsCycle chain :=
  R2VertexParityBoundaryData.fillable_isCycle
    K.toVertexParityBoundaryData
    Adm
    chain
    hFillable

end R2EndpointBoundaryData

end Frontier
end Chronos
