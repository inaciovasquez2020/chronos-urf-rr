import Chronos.Frontier.H4_1_FGL_ObservationExtractionWitnessInterface

universe u v

namespace Chronos
namespace Frontier

/--
Semantic final-carrier data for the H4.1/FGL observation-extraction layer.

Unlike the earlier proposition-valued witness interface, this object contains
actual carrier and observation types, predicates on the carrier, and a predicate
on observations.
-/
structure H4_1_FGL_SemanticFinalCarrier where
  Carrier : Type u
  Observation : Type v
  FinalHypothesis : Carrier → Prop
  FinalGapLeft : Carrier → Prop
  FinalGapRight : Carrier → Prop
  SoundnessPredicate : Carrier → Prop
  ObsSoundnessPredicate : Observation → Prop

/--
A semantic observation map on a selected final carrier.

The map is semantic because `observe` is an actual function from carriers to
observations, and the separation/soundness clauses are predicates about that
function.
-/
structure H4_1_FGL_SemanticObservationMap
    (S : H4_1_FGL_SemanticFinalCarrier.{u, v}) where
  observe : S.Carrier → S.Observation
  separates_final_gap :
    ∀ x y : S.Carrier,
      S.FinalGapLeft x →
      S.FinalGapRight y →
      observe x ≠ observe y
  preserves_selected_carrier_soundness :
    ∀ x : S.Carrier,
      S.FinalHypothesis x →
      S.SoundnessPredicate x →
      S.ObsSoundnessPredicate (observe x)

/--
The weakest semantic input needed to construct an observation map:
an explicit separating observable.
-/
structure H4_1_FGL_SemanticSeparatingObservable
    (S : H4_1_FGL_SemanticFinalCarrier.{u, v}) where
  toObservation : S.Carrier → S.Observation
  separates_final_gap :
    ∀ x y : S.Carrier,
      S.FinalGapLeft x →
      S.FinalGapRight y →
      toObservation x ≠ toObservation y
  preserves_selected_carrier_soundness :
    ∀ x : S.Carrier,
      S.FinalHypothesis x →
      S.SoundnessPredicate x →
      S.ObsSoundnessPredicate (toObservation x)

/--
Semantic observation-map construction from an explicit separating observable.
-/
def h4_1_fgl_construct_semantic_observation_map
    (S : H4_1_FGL_SemanticFinalCarrier.{u, v})
    (W : H4_1_FGL_SemanticSeparatingObservable S) :
    H4_1_FGL_SemanticObservationMap S :=
{
  observe := W.toObservation,
  separates_final_gap := W.separates_final_gap,
  preserves_selected_carrier_soundness :=
    W.preserves_selected_carrier_soundness
}

/--
A complete semantic package: a selected final-carrier point and a constructed
semantic observation map.
-/
structure H4_1_FGL_SemanticObservationConstructionPackage where
  S : H4_1_FGL_SemanticFinalCarrier.{u, v}
  selected_witness : S.Carrier
  selected_witness_selected : S.FinalHypothesis selected_witness
  observation_map : H4_1_FGL_SemanticObservationMap S

/--
Build the complete semantic package from an explicit separating observable and
one selected final-carrier point.
-/
def H4_1_FGL_SemanticObservationConstructionPackage.ofSeparatingObservable
    (S : H4_1_FGL_SemanticFinalCarrier.{u, v})
    (selected_witness : S.Carrier)
    (selected_witness_selected : S.FinalHypothesis selected_witness)
    (W : H4_1_FGL_SemanticSeparatingObservable S) :
    H4_1_FGL_SemanticObservationConstructionPackage :=
{
  S := S,
  selected_witness := selected_witness,
  selected_witness_selected := selected_witness_selected,
  observation_map := h4_1_fgl_construct_semantic_observation_map S W
}

/--
Convert a semantic observation package into the previous proposition-valued
interface witness.
-/
def H4_1_FGL_SemanticObservationConstructionPackage.toPropWitness
    (P : H4_1_FGL_SemanticObservationConstructionPackage.{u, v}) :
    H4_1_FGL_ObservationExtractionWitness :=
{
  selected_final_carrier_domain :=
    ∃ x : P.S.Carrier, P.S.FinalHypothesis x,
  observation_map_exists :=
    Nonempty (H4_1_FGL_SemanticObservationMap P.S),
  observation_separates_final_carrier_gap :=
    ∀ x y : P.S.Carrier,
      P.S.FinalGapLeft x →
      P.S.FinalGapRight y →
      P.observation_map.observe x ≠ P.observation_map.observe y,
  observation_preserves_selected_carrier_soundness :=
    ∀ x : P.S.Carrier,
      P.S.FinalHypothesis x →
      P.S.SoundnessPredicate x →
      P.S.ObsSoundnessPredicate (P.observation_map.observe x)
}

/--
A semantic observation-map package implies the original missing
proposition-valued witness target.
-/
theorem h4_1_fgl_semantic_observation_package_implies_missing_witness
    (P : H4_1_FGL_SemanticObservationConstructionPackage.{u, v}) :
    H4_1_FGL_MissingObservationExtractionWitness := by
  refine
    ⟨H4_1_FGL_SemanticObservationConstructionPackage.toPropWitness P,
      ?_,
      ?_,
      ?_,
      ?_⟩
  · exact ⟨P.selected_witness, P.selected_witness_selected⟩
  · exact ⟨P.observation_map⟩
  · intro x y hx hy
    exact P.observation_map.separates_final_gap x y hx hy
  · intro x hx hs
    exact P.observation_map.preserves_selected_carrier_soundness x hx hs

/--
An explicit separating observable plus one selected final-carrier point implies
the original missing proposition-valued witness target.
-/
theorem h4_1_fgl_semantic_separating_observable_implies_missing_witness
    (S : H4_1_FGL_SemanticFinalCarrier.{u, v})
    (selected_witness : S.Carrier)
    (selected_witness_selected : S.FinalHypothesis selected_witness)
    (W : H4_1_FGL_SemanticSeparatingObservable S) :
    H4_1_FGL_MissingObservationExtractionWitness := by
  exact
    h4_1_fgl_semantic_observation_package_implies_missing_witness
      (H4_1_FGL_SemanticObservationConstructionPackage.ofSeparatingObservable
        S selected_witness selected_witness_selected W)

/--
Conditional boundary: this file constructs a semantic observation map from an
explicit separating observable. It does not prove that such an observable exists
for every selected final-carrier instance.
-/
theorem h4_1_fgl_semantic_observation_map_construction_boundary :
    True := by
  trivial

end Frontier
end Chronos
