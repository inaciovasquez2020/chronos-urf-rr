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
The concrete observational equivalence relation on selected admissible
histories.

Two histories represent the same quotient point exactly when all four
repository-native vertex observables agree. This relation is derived from the
executable observables; it does not assume an equivalence with an independently
specified external carrier.
-/
def h41FGLK4SelectedAdmissibleHistoryObservableSetoid :
    Setoid H41FGLK4SelectedAdmissibleHistory where
  r h₁ h₂ :=
    ∀ i : Fin 4,
      h41FGLK4SelectedAdmissibleHistoryObservable i h₁ =
        h41FGLK4SelectedAdmissibleHistoryObservable i h₂
  iseqv := by
    constructor
    · intro history i
      rfl
    · intro h₁ h₂ hcoordinates i
      exact (hcoordinates i).symm
    · intro h₁ h₂ h₃ h₁₂ h₂₃ i
      exact (h₁₂ i).trans (h₂₃ i)

/--
The concrete quotient of selected admissible histories by equality of all four
repository-native vertex observables.

This quotient is defined entirely from the executable selected-history model.
It is not yet identified with the externally intended `X(𝒫_{4,0,1})`.
-/
abbrev H41FGLK4SelectedAdmissibleHistoryObservableQuotient : Type :=
  Quotient h41FGLK4SelectedAdmissibleHistoryObservableSetoid

/--
The canonical projection from a selected admissible history to its
observational-equivalence class.
-/
def h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk
    (history : H41FGLK4SelectedAdmissibleHistory) :
    H41FGLK4SelectedAdmissibleHistoryObservableQuotient :=
  Quotient.mk
    h41FGLK4SelectedAdmissibleHistoryObservableSetoid
    history

/--
The vertex observable at coordinate zero descended to the concrete
observational quotient.
-/
def h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservableZero
    (historyClass :
      H41FGLK4SelectedAdmissibleHistoryObservableQuotient) :
    ZMod 2 :=
  Quotient.lift
    (fun history =>
      h41FGLK4SelectedAdmissibleHistoryObservable
        (0 : Fin 4)
        history)
    (by
      intro h₁ h₂ hrelated
      exact hrelated (0 : Fin 4))
    historyClass

/--
The descended coordinate-zero observable evaluates on a projected
representative as the original coordinate-zero observable.
-/
theorem
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservableZero_mk
    (history : H41FGLK4SelectedAdmissibleHistory) :
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservableZero
        (h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk history) =
      h41FGLK4SelectedAdmissibleHistoryObservable
        (0 : Fin 4)
        history := by
  rfl

/--
The uniformly descended vertex observable on the concrete observational
quotient.
-/
def h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservable
    (i : Fin 4)
    (historyClass :
      H41FGLK4SelectedAdmissibleHistoryObservableQuotient) :
    ZMod 2 :=
  Quotient.lift
    (fun history =>
      h41FGLK4SelectedAdmissibleHistoryObservable i history)
    (by
      intro h₁ h₂ hrelated
      exact hrelated i)
    historyClass

/--
Every uniformly descended quotient observable evaluates on a projected
representative as the corresponding original vertex observable.
-/
theorem h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservable_mk
    (i : Fin 4)
    (history : H41FGLK4SelectedAdmissibleHistory) :
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservable
        i
        (h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk history) =
      h41FGLK4SelectedAdmissibleHistoryObservable i history := by
  rfl

/--
Observational equivalence identifies no distinct selected admissible histories.

Equality of all four quotient-defining observables implies equality of the
underlying histories by the established vertex-extensionality theorem.
-/
theorem
    h41FGLK4SelectedAdmissibleHistoryObservableSetoid_rel_implies_eq
    {h₁ h₂ : H41FGLK4SelectedAdmissibleHistory}
    (hrelated :
      (h41FGLK4SelectedAdmissibleHistoryObservableSetoid).r h₁ h₂) :
    h₁ = h₂ := by
  exact
    h41FGLK4SelectedAdmissibleHistory_vertexExt
      h₁
      h₂
      hrelated

/--
The canonical projection to the observational quotient is injective.

Equality of projected classes forces equality of every descended coordinate.
The representative equations then recover equality of the four original
observables, so vertex extensionality recovers equality of histories.
-/
theorem
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk_injective :
    Function.Injective
      h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk := by
  intro h₁ h₂ hclasses
  apply h41FGLK4SelectedAdmissibleHistory_vertexExt
  intro i
  calc
    h41FGLK4SelectedAdmissibleHistoryObservable i h₁ =
        h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservable
          i
          (h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk h₁) :=
      (h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservable_mk
        i
        h₁).symm
    _ =
        h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservable
          i
          (h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk h₂) := by
      exact
        congrArg
          (h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservable i)
          hclasses
    _ = h41FGLK4SelectedAdmissibleHistoryObservable i h₂ :=
      h41FGLK4SelectedAdmissibleHistoryObservableQuotientObservable_mk
        i
        h₂

/--
The canonical projection to the observational quotient is surjective.

Every quotient class is represented by an underlying selected admissible
history.
-/
theorem
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk_surjective :
    Function.Surjective
      h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk := by
  intro historyClass
  refine Quotient.inductionOn historyClass ?_
  intro history
  exact ⟨history, rfl⟩

/--
The selected admissible-history carrier is explicitly equivalent to its
observational quotient.

This is an internal equivalence induced by the proved bijectivity of the
canonical quotient projection. It does not identify either carrier with the
externally intended `X(𝒫_{4,0,1})`.
-/
noncomputable def
    h41FGLK4SelectedAdmissibleHistoryEquivObservableQuotient :
    H41FGLK4SelectedAdmissibleHistory ≃
      H41FGLK4SelectedAdmissibleHistoryObservableQuotient :=
  Equiv.ofBijective
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk
    ⟨
      h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk_injective,
      h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk_surjective
    ⟩

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
The local-type value on the observational quotient, transported through the
inverse of the internal selected-history/quotient equivalence.
-/
noncomputable def
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientLocalType
    (historyClass :
      H41FGLK4SelectedAdmissibleHistoryObservableQuotient) :
    Nat :=
  h41FGLK4SelectedAdmissibleHistoryLocalType
    (h41FGLK4SelectedAdmissibleHistoryEquivObservableQuotient.symm
      historyClass)

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
Every observational quotient class has transported local-type value at most
four.
-/
theorem
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientLocalType_le_four
    (historyClass :
      H41FGLK4SelectedAdmissibleHistoryObservableQuotient) :
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientLocalType
        historyClass ≤
      4 := by
  simpa [
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientLocalType
  ] using
    h41FGLK4SelectedAdmissibleHistoryLocalType_le_four
      (h41FGLK4SelectedAdmissibleHistoryEquivObservableQuotient.symm
        historyClass)

/--
R3 semantic data carried by the concrete observational quotient of selected K4
admissible histories.

The quotient local type is transported through the proved internal
selected-history/quotient equivalence, and its capacity is four. The
factorisation predicate records that the quotient class has a selected-history
representative.

This package remains internal and does not identify the quotient with the
externally intended `X(𝒫_{4,0,1})`.
-/
noncomputable def
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientR3SemanticData :
    R3SemanticData where
  QuotientData :=
    H41FGLK4SelectedAdmissibleHistoryObservableQuotient
  C := 4
  dim :=
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientLocalType
  FactorsThroughBoundedLocalType := fun historyClass =>
    ∃ history : H41FGLK4SelectedAdmissibleHistory,
      h41FGLK4SelectedAdmissibleHistoryObservableQuotientMk history =
        historyClass

/--
The observational-quotient R3 semantic package satisfies its uniform
local-type capacity theorem.
-/
theorem
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientR3SemanticData_correct :
    R3UniformLocalTypeCapacityTheorem
      h41FGLK4SelectedAdmissibleHistoryObservableQuotientR3SemanticData := by
  intro historyClass _hfactor
  exact
    h41FGLK4SelectedAdmissibleHistoryObservableQuotientLocalType_le_four
      historyClass

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
