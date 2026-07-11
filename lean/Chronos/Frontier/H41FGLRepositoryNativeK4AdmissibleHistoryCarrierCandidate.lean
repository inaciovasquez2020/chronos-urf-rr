import Chronos.Frontier.H41FGLRepositoryNativeK4VertexAssignmentCarrierCandidate

namespace Chronos
namespace Frontier

/--
The active global vertices of a bounded K4 vertex-assignment history.
-/
def H41FGLK4ActiveHistoryVertices
    (history : H41FGLK4VertexAssignmentHistory) :
    Finset (H41FGLAffineLiftK4Vertex 0 1) :=
  Finset.univ.filter fun vertex => history vertex ≠ 0

/--
A bounded selected-history admissibility predicate.

A history is admissible when its active support touches at most four global
vertices. This is a concrete repository-native selected model; it is not an
identification with the externally intended `X(𝒫_{4,0,1})`.
-/
def H41FGLK4SelectedHistoryAdmissible
    (history : H41FGLK4VertexAssignmentHistory) :
    Prop :=
  (H41FGLK4ActiveHistoryVertices history).card ≤ 4

/--
The independently specified bounded selected admissible-history carrier.
-/
abbrev H41FGLK4SelectedAdmissibleHistory : Type :=
  {history : H41FGLK4VertexAssignmentHistory //
    H41FGLK4SelectedHistoryAdmissible history}

/--
Every history on the radius-zero, one-patch K4 candidate satisfies the
four-vertex support bound.
-/
theorem h41FGLK4SelectedHistoryAdmissible_all
    (history : H41FGLK4VertexAssignmentHistory) :
    H41FGLK4SelectedHistoryAdmissible history := by
  unfold H41FGLK4SelectedHistoryAdmissible
  have hsubset :
      H41FGLK4ActiveHistoryVertices history ⊆
        (Finset.univ :
          Finset (H41FGLAffineLiftK4Vertex 0 1)) := by
    intro vertex hvertex
    simp
  calc
    (H41FGLK4ActiveHistoryVertices history).card
        ≤
      (Finset.univ :
        Finset (H41FGLAffineLiftK4Vertex 0 1)).card :=
      Finset.card_le_card hsubset
    _ = 4 := by native_decide

/-- Evaluation of a selected admissible history at K4 vertex `i`. -/
def h41FGLK4SelectedAdmissibleHistoryObservable
    (i : Fin 4)
    (history : H41FGLK4SelectedAdmissibleHistory) :
    ZMod 2 :=
  h41FGLK4VertexAssignmentObservable i history.1

/-- Construct the selected admissible history prescribed by four bits. -/
def h41FGLK4SelectedAdmissibleHistoryOfBits
    (σ : H41FGLK4BitVector) :
    H41FGLK4SelectedAdmissibleHistory :=
  ⟨h41FGLK4VertexAssignmentHistoryOfBits σ,
    h41FGLK4SelectedHistoryAdmissible_all
      (h41FGLK4VertexAssignmentHistoryOfBits σ)⟩

/-- The selected admissible construction realizes every prescribed bit. -/
theorem h41FGLK4SelectedAdmissibleHistoryObservable_historyOfBits
    (σ : H41FGLK4BitVector)
    (i : Fin 4) :
    h41FGLK4SelectedAdmissibleHistoryObservable
        i
        (h41FGLK4SelectedAdmissibleHistoryOfBits σ) =
      σ i :=
  rfl

/-- The four observables determine a selected admissible history. -/
theorem h41FGLK4SelectedAdmissibleHistory_vertexExt
    (h₁ h₂ : H41FGLK4SelectedAdmissibleHistory)
    (hcoordinates :
      ∀ i : Fin 4,
        h41FGLK4SelectedAdmissibleHistoryObservable i h₁ =
          h41FGLK4SelectedAdmissibleHistoryObservable i h₂) :
    h₁ = h₂ := by
  apply Subtype.ext
  apply h41FGLK4VertexAssignment_vertexExt
  intro i
  simpa [h41FGLK4SelectedAdmissibleHistoryObservable] using
    hcoordinates i

/--
The carrier predicate for the concrete selected admissible-history model.

It does not assert identification with the external admissible-history space.
-/
def H41FGLIsK4SelectedAdmissibleHistoryCarrier
    (History : Type) :
    Prop :=
  Nonempty (History ≃ H41FGLK4SelectedAdmissibleHistory)

/--
A completed carrier construction for the explicit selected admissible-history
model.
-/
def h41FGLK4SelectedAdmissibleHistoryCarrierConstruction :
    H41FGLRepositoryNativeK4CarrierConstruction
      H41FGLIsK4SelectedAdmissibleHistoryCarrier where
  History := H41FGLK4SelectedAdmissibleHistory
  repository_native := ⟨Equiv.refl _⟩
  vertexObservable :=
    h41FGLK4SelectedAdmissibleHistoryObservable
  historyOfBits :=
    h41FGLK4SelectedAdmissibleHistoryOfBits
  vertexObservable_historyOfBits :=
    h41FGLK4SelectedAdmissibleHistoryObservable_historyOfBits
  vertex_ext :=
    h41FGLK4SelectedAdmissibleHistory_vertexExt

end Frontier
end Chronos
