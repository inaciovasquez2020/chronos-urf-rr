import Chronos.Frontier.H4_1_FGL_SemanticObservationMapConstruction

universe u v

namespace Chronos
namespace Frontier

/--
Selected final-carrier instance data sufficient to construct a semantic
separating observable.

This is the non-tautological structural layer needed after the semantic
observation-map construction: the final gap sides are disjoint, the two sides
have distinct admissible observations, and non-gap points have a default
admissible observation.
-/
structure H4_1_FGL_SelectedFinalCarrierInstance
    (S : H4_1_FGL_SemanticFinalCarrier.{u, v}) where
  leftObs : S.Observation
  rightObs : S.Observation
  defaultObs : S.Observation
  left_right_distinct : leftObs ≠ rightObs
  leftObs_sound : S.ObsSoundnessPredicate leftObs
  rightObs_sound : S.ObsSoundnessPredicate rightObs
  defaultObs_sound : S.ObsSoundnessPredicate defaultObs
  gap_disjoint :
    ∀ z : S.Carrier,
      S.FinalGapLeft z →
      S.FinalGapRight z →
      False
  left_decidable : DecidablePred S.FinalGapLeft
  right_decidable : DecidablePred S.FinalGapRight

namespace H4_1_FGL_SelectedFinalCarrierInstance

/--
The explicit semantic observation function induced by selected final-carrier
separation data.
-/
def observe
    {S : H4_1_FGL_SemanticFinalCarrier.{u, v}}
    (I : H4_1_FGL_SelectedFinalCarrierInstance S)
    (x : S.Carrier) : S.Observation :=
  letI : Decidable (S.FinalGapLeft x) := I.left_decidable x
  letI : Decidable (S.FinalGapRight x) := I.right_decidable x
  if hL : S.FinalGapLeft x then
    I.leftObs
  else if hR : S.FinalGapRight x then
    I.rightObs
  else
    I.defaultObs

/--
Selected final-carrier separation data constructs an explicit semantic
separating observable.
-/
def toSeparatingObservable
    {S : H4_1_FGL_SemanticFinalCarrier.{u, v}}
    (I : H4_1_FGL_SelectedFinalCarrierInstance S) :
    H4_1_FGL_SemanticSeparatingObservable S :=
{
  toObservation := observe I,
  separates_final_gap := by
    intro x y hx hy
    have hy_not_left : ¬ S.FinalGapLeft y := by
      intro hy_left
      exact I.gap_disjoint y hy_left hy
    simpa [observe, hx, hy_not_left, hy] using I.left_right_distinct
  preserves_selected_carrier_soundness := by
    intro x hx hs
    haveI : Decidable (S.FinalGapLeft x) := I.left_decidable x
    haveI : Decidable (S.FinalGapRight x) := I.right_decidable x
    by_cases hL : S.FinalGapLeft x
    · simpa [observe, hL] using I.leftObs_sound
    · by_cases hR : S.FinalGapRight x
      · simpa [observe, hL, hR] using I.rightObs_sound
      · simpa [observe, hL, hR] using I.defaultObs_sound
}

/--
Every selected final-carrier instance has an explicit separating observable.
-/
theorem has_separating_observable
    {S : H4_1_FGL_SemanticFinalCarrier.{u, v}}
    (I : H4_1_FGL_SelectedFinalCarrierInstance S) :
    Nonempty (H4_1_FGL_SemanticSeparatingObservable S) := by
  exact ⟨toSeparatingObservable I⟩

end H4_1_FGL_SelectedFinalCarrierInstance

/--
Predicate form of selected final-carrier instancehood.
-/
def H4_1_FGL_SelectedFinalCarrierInstancePredicate
    (S : H4_1_FGL_SemanticFinalCarrier.{u, v}) : Prop :=
  Nonempty (H4_1_FGL_SelectedFinalCarrierInstance S)

/--
Universal selected-instance existence theorem.

Every selected final-carrier instance has an explicit semantic separating
observable.
-/
theorem H4_1_FGL_SelectedFinalCarrierSeparatingObservableExistence :
    ∀ S : H4_1_FGL_SemanticFinalCarrier.{u, v},
      H4_1_FGL_SelectedFinalCarrierInstancePredicate S →
      Nonempty (H4_1_FGL_SemanticSeparatingObservable S) := by
  intro S hS
  rcases hS with ⟨I⟩
  exact H4_1_FGL_SelectedFinalCarrierInstance.has_separating_observable I

/--
Selected final-carrier instance with one selected point, sufficient to feed the
semantic observation-map package theorem.
-/
structure H4_1_FGL_SelectedFinalCarrierInstanceWithPoint
    (S : H4_1_FGL_SemanticFinalCarrier.{u, v}) where
  separation : H4_1_FGL_SelectedFinalCarrierInstance S
  selected_witness : S.Carrier
  selected_witness_selected : S.FinalHypothesis selected_witness

/--
A selected final-carrier instance with a selected point closes the semantic
observation-extraction witness target through the previously constructed
semantic observation-map bridge.
-/
theorem H4_1_FGL_SelectedFinalCarrierInstanceWithPoint_implies_missing_witness
    {S : H4_1_FGL_SemanticFinalCarrier.{u, v}}
    (I : H4_1_FGL_SelectedFinalCarrierInstanceWithPoint S) :
    H4_1_FGL_MissingObservationExtractionWitness := by
  exact
    h4_1_fgl_semantic_separating_observable_implies_missing_witness
      S
      I.selected_witness
      I.selected_witness_selected
      (H4_1_FGL_SelectedFinalCarrierInstance.toSeparatingObservable I.separation)

/--
Boundary: this proves separating-observable existence for selected final-carrier
instances carrying the stated separation data. It does not prove existence for arbitrary semantic final carriers.
-/
theorem h4_1_fgl_selected_separating_observable_existence_boundary :
    True := by
  trivial

end Frontier
end Chronos
