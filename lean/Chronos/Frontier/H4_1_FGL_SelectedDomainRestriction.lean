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
    ¬ (∀ S : H4_1_FGL_SemanticFinalCarrier.{0, 0},
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
    ¬ (∀ S : H4_1_FGL_SemanticFinalCarrier.{0, 0},
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

namespace Chronos
namespace Frontier

/--
Boundary vocabulary required before stating
`SELECTED_DOMAIN_DEFECT_REPAIR_TO_REALIZABLE_NORMALIZATION`.

This introduces vocabulary only, grounded in the selected-domain restriction
surface. It does not prove repair, normalization, terminal closure, or selected
representability.
-/
abbrev W_unrestricted : Type 1 :=
  H4_1_FGL_SemanticFinalCarrier.{0, 0}

abbrev W_T : Type 1 :=
  H4_1_FGL_SelectedTheoremDomain.{0, 0}

def terminal_unrestricted (_w : W_unrestricted) : Prop :=
  True

def selected_domain_representable (_w : W_unrestricted) : Prop :=
  True

def selected_domain_realizable (_w : W_unrestricted) : Prop :=
  True

def selected_domain (_nf : W_T) : Prop :=
  True

def terminal_T (_nf : W_T) : Prop :=
  True

def represents_terminal (_nf : W_T) (_w : W_unrestricted) : Prop :=
  True

def normalization_relation (_w : W_unrestricted) (_nf : W_T) : Prop :=
  True

def SELECTED_DOMAIN_DEFECT_REPAIR_TO_REALIZABLE_NORMALIZATION_BOUNDARY : Prop :=
  ∀ w : W_unrestricted,
    terminal_unrestricted w →
    selected_domain_representable w →
    ∃ w' : W_unrestricted,
        selected_domain_realizable w'
      ∧ terminal_unrestricted w'
      ∧ ∃ nf : W_T,
          represents_terminal nf w
        ∧ normalization_relation w nf

end Frontier
end Chronos
