namespace Chronos
namespace Frontier

/--
Witness interface for reducing the H4.1/FGL final-carrier observation extraction
frontier to explicit witness data.
-/
structure H4_1_FGL_ObservationExtractionWitness where
  selected_final_carrier_domain : Prop
  observation_map_exists : Prop
  observation_separates_final_carrier_gap : Prop
  observation_preserves_selected_carrier_soundness : Prop

/--
The theorem-level extraction obligation as a proposition-level target.
-/
def H4_1_FGL_FinalCarrierObservationExtractionTarget : Prop :=
  ∃ W : H4_1_FGL_ObservationExtractionWitness,
    W.selected_final_carrier_domain ∧
    W.observation_map_exists ∧
    W.observation_separates_final_carrier_gap ∧
    W.observation_preserves_selected_carrier_soundness

/--
A complete observation-extraction witness implies the final-carrier observation
extraction target.
-/
theorem h4_1_fgl_observation_extraction_witness_implies_target
    (W : H4_1_FGL_ObservationExtractionWitness)
    (h_domain : W.selected_final_carrier_domain)
    (h_map : W.observation_map_exists)
    (h_sep : W.observation_separates_final_carrier_gap)
    (h_sound : W.observation_preserves_selected_carrier_soundness) :
    H4_1_FGL_FinalCarrierObservationExtractionTarget := by
  exact ⟨W, h_domain, h_map, h_sep, h_sound⟩

/--
The remaining missing ingredient after this interface is explicit construction of
the witness W.
-/
def H4_1_FGL_MissingObservationExtractionWitness : Prop :=
  ∃ W : H4_1_FGL_ObservationExtractionWitness,
    W.selected_final_carrier_domain ∧
    W.observation_map_exists ∧
    W.observation_separates_final_carrier_gap ∧
    W.observation_preserves_selected_carrier_soundness

theorem h4_1_fgl_missing_witness_equiv_target :
    H4_1_FGL_MissingObservationExtractionWitness ↔
    H4_1_FGL_FinalCarrierObservationExtractionTarget := by
  rfl

end Frontier
end Chronos
