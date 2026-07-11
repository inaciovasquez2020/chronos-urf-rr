import Chronos.Frontier.H41FGLRepositoryNativeK4CarrierConstructionBoundary

namespace Chronos
namespace Frontier

/--
A concrete candidate history carrier on the repository's existing radius-zero,
one-patch affine-lift `K₄` vertex type.

A history assigns one Boolean value to each encoded global `K₄` vertex.

This is an independently defined bounded candidate. No theorem here identifies
it with the externally intended admissible-history space
`X(𝒫_{4,0,1})`.
-/
abbrev H41FGLK4VertexAssignmentHistory : Type :=
  H41FGLAffineLiftK4Vertex 0 1 → ZMod 2

/-- The unique radius-zero, one-patch global vertex with local index `i`. -/
def h41FGLK4VertexAt
    (i : Fin 4) :
    H41FGLAffineLiftK4Vertex 0 1 where
  patch := 0
  layer := 0
  localVertex := i

/-- Evaluation of a candidate history at local `K₄` vertex `i`. -/
def h41FGLK4VertexAssignmentObservable
    (i : Fin 4)
    (history : H41FGLK4VertexAssignmentHistory) :
    ZMod 2 :=
  history (h41FGLK4VertexAt i)

/-- Construct the candidate history prescribed by four Boolean coordinates. -/
def h41FGLK4VertexAssignmentHistoryOfBits
    (σ : H41FGLK4BitVector) :
    H41FGLK4VertexAssignmentHistory :=
  fun vertex => σ vertex.localVertex

/-- The constructed candidate history realizes each prescribed coordinate. -/
theorem h41FGLK4VertexAssignmentObservable_historyOfBits
    (σ : H41FGLK4BitVector)
    (i : Fin 4) :
    h41FGLK4VertexAssignmentObservable
        i
        (h41FGLK4VertexAssignmentHistoryOfBits σ) =
      σ i :=
  rfl

/--
The bounded candidate-carrier predicate records equivalence with the concrete
vertex-assignment history type.

It does not assert equivalence with the external admissible-history space.
-/
def H41FGLIsK4VertexAssignmentCarrier
    (History : Type) :
    Prop :=
  Nonempty (History ≃ H41FGLK4VertexAssignmentHistory)

/--
The four coordinate evaluations determine a candidate vertex-assignment
history because the patch and layer index types are both singletons.
-/
theorem h41FGLK4VertexAssignment_vertexExt
    (h₁ h₂ : H41FGLK4VertexAssignmentHistory)
    (hcoordinates :
      ∀ i : Fin 4,
        h41FGLK4VertexAssignmentObservable i h₁ =
          h41FGLK4VertexAssignmentObservable i h₂) :
    h₁ = h₂ := by
  funext vertex
  rcases vertex with ⟨patch, layer, localVertex⟩
  fin_cases patch
  fin_cases layer
  simpa [
    h41FGLK4VertexAssignmentObservable,
    h41FGLK4VertexAt
  ] using hcoordinates localVertex

/--
A completed carrier construction for the concrete bounded
vertex-assignment candidate.

This construction does not discharge identification with
`X(𝒫_{4,0,1})`.
-/
def h41FGLK4VertexAssignmentCarrierConstruction :
    H41FGLRepositoryNativeK4CarrierConstruction
      H41FGLIsK4VertexAssignmentCarrier where
  History := H41FGLK4VertexAssignmentHistory
  repository_native := ⟨Equiv.refl _⟩
  vertexObservable :=
    h41FGLK4VertexAssignmentObservable
  historyOfBits :=
    h41FGLK4VertexAssignmentHistoryOfBits
  vertexObservable_historyOfBits :=
    h41FGLK4VertexAssignmentObservable_historyOfBits
  vertex_ext :=
    h41FGLK4VertexAssignment_vertexExt

/--
The completed bounded vertex-assignment carrier construction inherits
injectivity of the transported sixteen-state K4 Walsh transform.

This theorem remains confined to the concrete candidate carrier and does not
identify it with the external admissible-history space `X(𝒫_{4,0,1})`.
-/
theorem h41FGLK4VertexAssignmentWalshTransform_injective :
    Function.Injective
      (H41FGLRepositoryNativeK4HistoryRealizability.repositoryNativeK4WalshTransform
        (H41FGLRepositoryNativeK4CarrierConstruction.toRealizability
          h41FGLK4VertexAssignmentCarrierConstruction)
        (H41FGLRepositoryNativeK4CarrierConstruction.toRealizability_vertexExt
          h41FGLK4VertexAssignmentCarrierConstruction)) := by
  exact
    H41FGLRepositoryNativeK4CarrierConstruction.repositoryNativeK4WalshTransform_injective
      h41FGLK4VertexAssignmentCarrierConstruction

end Frontier
end Chronos
