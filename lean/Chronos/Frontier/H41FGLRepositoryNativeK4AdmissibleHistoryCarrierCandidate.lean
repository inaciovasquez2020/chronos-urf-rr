import Chronos.Frontier.H41FGLRepositoryNativeK4VertexAssignmentCarrierCandidate
import Chronos.Frontier.R1R2R3SemanticTheoremProofTargets

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

/--
At the bounded `(k, R, B) = (4, 0, 1)` parameter choice, the selected
support-cardinality admissibility predicate imposes no further restriction:
every candidate history is admissible.
-/
theorem h41FGLK4SelectedHistoryAdmissible_iff_true
    (history : H41FGLK4VertexAssignmentHistory) :
    H41FGLK4SelectedHistoryAdmissible history ↔ True := by
  constructor
  · intro _
    trivial
  · intro _
    exact h41FGLK4SelectedHistoryAdmissible_all history

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
The selected admissible-history carrier has at least two distinct explicit
histories, witnessed by the constant-zero and constant-one K4 bit vectors.
-/
theorem h41FGLK4SelectedAdmissibleHistory_two_distinct :
    ∃ h0 h1 : H41FGLK4SelectedAdmissibleHistory, h0 ≠ h1 := by
  let sigma0 : H41FGLK4BitVector := fun _ => 0
  let sigma1 : H41FGLK4BitVector := fun _ => 1
  refine ⟨
    h41FGLK4SelectedAdmissibleHistoryOfBits sigma0,
    h41FGLK4SelectedAdmissibleHistoryOfBits sigma1,
    ?_⟩
  intro historiesEqual
  have observablesEqual :=
    congrArg
      (h41FGLK4SelectedAdmissibleHistoryObservable (0 : Fin 4))
      historiesEqual
  have zeroEqualsOne : (0 : ZMod 2) = 1 := by
    calc
      (0 : ZMod 2) = sigma0 (0 : Fin 4) := by rfl
      _ =
          h41FGLK4SelectedAdmissibleHistoryObservable
            (0 : Fin 4)
            (h41FGLK4SelectedAdmissibleHistoryOfBits sigma0) :=
        (h41FGLK4SelectedAdmissibleHistoryObservable_historyOfBits
          sigma0
          (0 : Fin 4)).symm
      _ =
          h41FGLK4SelectedAdmissibleHistoryObservable
            (0 : Fin 4)
            (h41FGLK4SelectedAdmissibleHistoryOfBits sigma1) :=
        observablesEqual
      _ = sigma1 (0 : Fin 4) :=
        h41FGLK4SelectedAdmissibleHistoryObservable_historyOfBits
          sigma1
          (0 : Fin 4)
      _ = 1 := by rfl
  exact (by decide : (0 : ZMod 2) ≠ 1) zeroEqualsOne

/--
The repository-native local-type value of a selected K4 history is the
cardinality of its active global-vertex support.
-/
def h41FGLK4SelectedAdmissibleHistoryLocalType
    (history : H41FGLK4SelectedAdmissibleHistory) :
    Nat :=
  (H41FGLK4ActiveHistoryVertices history.1).card

/--
Every selected K4 admissible history has local-type value at most four.
-/
theorem h41FGLK4SelectedAdmissibleHistoryLocalType_le_four
    (history : H41FGLK4SelectedAdmissibleHistory) :
    h41FGLK4SelectedAdmissibleHistoryLocalType history ≤ 4 := by
  simpa [
    h41FGLK4SelectedAdmissibleHistoryLocalType,
    H41FGLK4SelectedHistoryAdmissible
  ] using history.2

/--
Repository-native selected-model R3 semantic data carried by bounded K4
admissible histories.

The dimension is active-support cardinality and the capacity is four. The
factorisation predicate records the existing selected-history admissibility
condition. This does not identify the carrier with the external quotient
`X(𝒫_{4,0,1})`.
-/
def h41FGLK4SelectedAdmissibleHistoryR3SemanticData :
    R3SemanticData where
  QuotientData := H41FGLK4SelectedAdmissibleHistory
  C := 4
  dim := h41FGLK4SelectedAdmissibleHistoryLocalType
  FactorsThroughBoundedLocalType := fun history =>
    H41FGLK4SelectedHistoryAdmissible history.1

/--
The selected-history R3 semantic package satisfies its uniform local-type
capacity theorem.
-/
theorem h41FGLK4SelectedAdmissibleHistoryR3SemanticData_correct :
    R3UniformLocalTypeCapacityTheorem
      h41FGLK4SelectedAdmissibleHistoryR3SemanticData := by
  intro history _hfactor
  exact
    h41FGLK4SelectedAdmissibleHistoryLocalType_le_four history

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

/--
The completed selected admissible-history carrier inherits injectivity of the
transported sixteen-state K4 Walsh transform.

This remains a theorem about the explicitly defined selected carrier and does
not identify it with the external admissible-history space
`X(𝒫_{4,0,1})`.
-/
theorem h41FGLK4SelectedAdmissibleHistoryWalshTransform_injective :
    Function.Injective
      (H41FGLRepositoryNativeK4HistoryRealizability.repositoryNativeK4WalshTransform
        (H41FGLRepositoryNativeK4CarrierConstruction.toRealizability
          h41FGLK4SelectedAdmissibleHistoryCarrierConstruction)
        (H41FGLRepositoryNativeK4CarrierConstruction.toRealizability_vertexExt
          h41FGLK4SelectedAdmissibleHistoryCarrierConstruction)) := by
  exact
    H41FGLRepositoryNativeK4CarrierConstruction.repositoryNativeK4WalshTransform_injective
      h41FGLK4SelectedAdmissibleHistoryCarrierConstruction

/--
Because bounded K4 admissibility is satisfied by every vertex-assignment
history, the selected admissible subtype is equivalent to its underlying
bounded vertex-assignment carrier.
-/
def h41FGLK4SelectedAdmissibleHistoryEquivVertexAssignment :
    H41FGLK4SelectedAdmissibleHistory ≃
      H41FGLK4VertexAssignmentHistory where
  toFun := Subtype.val
  invFun := fun history =>
    ⟨history, h41FGLK4SelectedHistoryAdmissible_all history⟩
  left_inv := by
    intro history
    apply Subtype.ext
    rfl
  right_inv := by
    intro history
    rfl

end Frontier
end Chronos
