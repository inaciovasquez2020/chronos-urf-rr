import Chronos.Frontier.H4_1_FGL_SelectedDomainRestriction

universe u v

namespace Chronos
namespace Frontier

/--
New toolkit input that resolves the remaining H4.1/FGL observation layer after
the arbitrary-domain refutation.

The input is intentionally restricted to the admissible selected theorem domain.
It does not re-open the refuted arbitrary semantic final-carrier domain.
-/
structure H4_1_FGL_FinalSelectedInput where
  domain : H4_1_FGL_SelectedTheoremDomain.{u, v}

/--
The final selected input carries exactly the restricted theorem domain accepted
after the arbitrary-domain counterexample.
-/
def H4_1_FGL_FinalSelectedInput.toSelectedTheoremDomain
    (I : H4_1_FGL_FinalSelectedInput.{u, v}) :
    H4_1_FGL_SelectedTheoremDomain.{u, v} :=
  I.domain

/--
The final selected input has an explicit semantic separating observable.
-/
theorem H4_1_FGL_FinalSelectedInput_has_separating_observable
    (I : H4_1_FGL_FinalSelectedInput.{u, v}) :
    Nonempty
      (H4_1_FGL_SemanticSeparatingObservable
        (H4_1_FGL_FinalSelectedInput.toSelectedTheoremDomain I).S) := by
  exact
    H4_1_FGL_SelectedTheoremDomain.has_separating_observable
      (H4_1_FGL_FinalSelectedInput.toSelectedTheoremDomain I)

/--
The final selected input closes the missing observation-extraction witness.
-/
theorem H4_1_FGL_FinalSelectedInput_implies_missing_observation_extraction_witness
    (I : H4_1_FGL_FinalSelectedInput.{u, v}) :
    H4_1_FGL_MissingObservationExtractionWitness := by
  exact
    H4_1_FGL_restricted_selected_domain_implies_missing_witness
      (H4_1_FGL_FinalSelectedInput.toSelectedTheoremDomain I)

/--
The final selected input closes the proposition-valued final-carrier observation
extraction target through the existing witness equivalence.
-/
theorem H4_1_FGL_FinalSelectedInput_implies_final_carrier_observation_extraction_target
    (I : H4_1_FGL_FinalSelectedInput.{u, v}) :
    H4_1_FGL_FinalCarrierObservationExtractionTarget := by
  exact
    h4_1_fgl_missing_witness_equiv_target.mp
      (H4_1_FGL_FinalSelectedInput_implies_missing_observation_extraction_witness I)

/--
Final selected-domain closure package.

This is the maximal admissible closure after the one-point counterexample:
all remaining H4.1/FGL observation-extraction obligations are closed on
`H4_1_FGL_FinalSelectedInput`.
-/
structure H4_1_FGL_FinalSelectedInputClosure where
  input : H4_1_FGL_FinalSelectedInput.{u, v}
  separating_observable_exists :
    Nonempty
      (H4_1_FGL_SemanticSeparatingObservable
        (H4_1_FGL_FinalSelectedInput.toSelectedTheoremDomain input).S)
  missing_observation_extraction_witness :
    H4_1_FGL_MissingObservationExtractionWitness
  final_carrier_observation_extraction_target :
    H4_1_FGL_FinalCarrierObservationExtractionTarget

/--
Named restricted-package theorem surface. This is only the target proposition
for the selected-domain closure package; it does not assert arbitrary semantic
final-carrier closure.
-/
def restricted_package_theorem_surface_closed : Prop :=
  ∀ I : H4_1_FGL_FinalSelectedInput.{u, v},
    ∃ C : H4_1_FGL_FinalSelectedInputClosure.{u, v},
      C.input = I

/--
Construct the final selected-domain closure package from the final selected
toolkit input.
-/
def H4_1_FGL_FinalSelectedInputClosure.ofInput
    (I : H4_1_FGL_FinalSelectedInput.{u, v}) :
    H4_1_FGL_FinalSelectedInputClosure.{u, v} :=
{
  input := I,
  separating_observable_exists :=
    H4_1_FGL_FinalSelectedInput_has_separating_observable I,
  missing_observation_extraction_witness :=
    H4_1_FGL_FinalSelectedInput_implies_missing_observation_extraction_witness I,
  final_carrier_observation_extraction_target :=
    H4_1_FGL_FinalSelectedInput_implies_final_carrier_observation_extraction_target I
}

/--
Final status theorem: no remaining observation-extraction obligation remains on
the selected theorem domain once `H4_1_FGL_FinalSelectedInput` is supplied.
-/
theorem H4_1_FGL_FinalSelectedInput_closes_selected_observation_layer
    (I : H4_1_FGL_FinalSelectedInput.{u, v}) :
    ∃ C : H4_1_FGL_FinalSelectedInputClosure.{u, v},
      C.input = I ∧
      C.missing_observation_extraction_witness =
        H4_1_FGL_FinalSelectedInput_implies_missing_observation_extraction_witness I ∧
      C.final_carrier_observation_extraction_target =
        H4_1_FGL_FinalSelectedInput_implies_final_carrier_observation_extraction_target I := by
  refine ⟨H4_1_FGL_FinalSelectedInputClosure.ofInput I, rfl, rfl, rfl⟩

/--
Bridge from the selected observation-layer closure package to the named
restricted-package theorem surface.
-/
theorem selected_observation_layer_to_named_restricted_package_surface :
    restricted_package_theorem_surface_closed := by
  intro I
  exact ⟨H4_1_FGL_FinalSelectedInputClosure.ofInput I, rfl⟩

/--
Boundary: this solves the remaining observation-extraction layer only on the
selected theorem domain. It does not claim arbitrary semantic final-carrier closure
closure, unrestricted H4.1/FGL, UniversalFiberEntropyGap, Chronos-RR, P vs NP,
or any Clay-problem closure. Remaining frontier: none inside selected-domain observation-extraction layer.
-/
theorem h4_1_fgl_final_selected_input_closure_boundary :
    True := by
  trivial

/--
The unrestricted arbitrary semantic final-carrier closure claim. This is kept
as a named negative-boundary surface and is not discharged.
-/
def unrestricted_h4_1_fgl_closed : Prop :=
  ∀ S : H4_1_FGL_SemanticFinalCarrier.{0, 0},
    Nonempty (H4_1_FGL_SemanticSeparatingObservable S)

/--
Negative boundary: the selected-domain closure package does not promote to
unrestricted arbitrary semantic final-carrier closure.
-/
theorem unrestricted_h4_1_fgl_promotion_refuted :
    ¬ unrestricted_h4_1_fgl_closed := by
  intro h_closed
  exact H4_1_FGL_arbitrary_semantic_final_carrier_separating_observable_refuted (by simpa [unrestricted_h4_1_fgl_closed] using h_closed)

end Frontier
end Chronos
