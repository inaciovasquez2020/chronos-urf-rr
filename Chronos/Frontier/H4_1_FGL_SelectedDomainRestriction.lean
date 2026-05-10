import Chronos.Frontier.H4_1_FGL_SelectedSeparatingObservableExistence

universe u v

namespace Chronos
namespace Frontier

/--
One-point semantic final carrier showing that arbitrary semantic final carriers
do not necessarily admit separating observables.
-/
def H4_1_FGL_ArbitrarySemanticFinalCarrierCounterexample :
    H4_1_FGL_SemanticFinalCarrier :=
{
  Carrier := Unit,
  Observation := Unit,
  FinalHypothesis := fun _ => True,
  FinalGapLeft := fun _ => True,
  FinalGapRight := fun _ => True,
  SoundnessPredicate := fun _ => True,
  ObsSoundnessPredicate := fun _ => True
}

/--
Arbitrary semantic final carriers do not all admit separating observables.

The one-point carrier has both gap sides true at the same point, so any
observation map would need to distinguish `()` from itself.
-/
theorem H4_1_FGL_arbitrary_semantic_final_carrier_separating_observable_refuted :
    ¬ (∀ S : H4_1_FGL_SemanticFinalCarrier,
        Nonempty (H4_1_FGL_SemanticSeparatingObservable S)) := by
  intro h
  rcases h H4_1_FGL_ArbitrarySemanticFinalCarrierCounterexample with ⟨W⟩
  have hbad :
      W.toObservation () ≠ W.toObservation () :=
    W.separates_final_gap () () True.intro True.intro
  exact hbad rfl

/--
Arbitrary semantic final carriers do not all satisfy selected-instance
separation data.
-/
theorem H4_1_FGL_arbitrary_semantic_final_carrier_selected_instance_refuted :
    ¬ (∀ S : H4_1_FGL_SemanticFinalCarrier,
        H4_1_FGL_SelectedFinalCarrierInstancePredicate S) := by
  intro h
  have hobs :
      Nonempty
        (H4_1_FGL_SemanticSeparatingObservable
          H4_1_FGL_ArbitrarySemanticFinalCarrierCounterexample) :=
    H4_1_FGL_SelectedFinalCarrierSeparatingObservableExistence
      H4_1_FGL_ArbitrarySemanticFinalCarrierCounterexample
      (h H4_1_FGL_ArbitrarySemanticFinalCarrierCounterexample)
  rcases hobs with ⟨W⟩
  have hbad :
      W.toObservation () ≠ W.toObservation () :=
    W.separates_final_gap () () True.intro True.intro
  exact hbad rfl

/--
Restricted theorem domain for the H4.1/FGL semantic observation layer.

This is the weakest admissible domain after the arbitrary-domain refutation:
a semantic final carrier, selected-instance separation data, and one selected
final-carrier point.
-/
structure H4_1_FGL_SelectedTheoremDomain where
  S : H4_1_FGL_SemanticFinalCarrier.{u, v}
  separation : H4_1_FGL_SelectedFinalCarrierInstance S
  selected_witness : S.Carrier
  selected_witness_selected : S.FinalHypothesis selected_witness

namespace H4_1_FGL_SelectedTheoremDomain

/--
Convert the restricted domain into the previously established selected-instance
with point object.
-/
def toInstanceWithPoint
    (D : H4_1_FGL_SelectedTheoremDomain.{u, v}) :
    H4_1_FGL_SelectedFinalCarrierInstanceWithPoint D.S :=
{
  separation := D.separation,
  selected_witness := D.selected_witness,
  selected_witness_selected := D.selected_witness_selected
}

/--
Every restricted-domain instance has an explicit separating observable.
-/
theorem has_separating_observable
    (D : H4_1_FGL_SelectedTheoremDomain.{u, v}) :
    Nonempty (H4_1_FGL_SemanticSeparatingObservable D.S) := by
  exact
    H4_1_FGL_SelectedFinalCarrierInstance.has_separating_observable
      D.separation

/--
Every restricted-domain instance yields the missing observation-extraction
witness.
-/
theorem implies_missing_observation_extraction_witness
    (D : H4_1_FGL_SelectedTheoremDomain.{u, v}) :
    H4_1_FGL_MissingObservationExtractionWitness := by
  exact
    H4_1_FGL_SelectedFinalCarrierInstanceWithPoint_implies_missing_witness
      (toInstanceWithPoint D)

end H4_1_FGL_SelectedTheoremDomain

/--
Final restricted-domain theorem statement for the current H4.1/FGL semantic
observation layer.
-/
theorem H4_1_FGL_restricted_selected_domain_implies_missing_witness
    (D : H4_1_FGL_SelectedTheoremDomain.{u, v}) :
    H4_1_FGL_MissingObservationExtractionWitness := by
  exact
    H4_1_FGL_SelectedTheoremDomain.implies_missing_observation_extraction_witness D

/--
Boundary: the arbitrary semantic-carrier domain is formally refuted, so the
theorem domain is restricted to selected final-carrier instances.
-/
theorem h4_1_fgl_selected_domain_restriction_boundary :
    True := by
  trivial

end Frontier
end Chronos
