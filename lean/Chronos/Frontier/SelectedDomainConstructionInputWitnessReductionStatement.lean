import Chronos.Frontier.SelectedDomainUnconditionalClosureConstructionInput
import Chronos.Frontier.SelectedDomainDefectAtomsConstructorTargetWitness

namespace Chronos
namespace Frontier

/--
The remaining semantic-prefix witness statement.

This is a statement only: it records that the selected-domain semantic-prefix
target exists. It does not construct that target.
-/
def selected_domain_semantic_prefix_witness_statement : Prop :=
  Nonempty
    SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix

/--
The final conditional closure bridge witness statement.

This is a statement only: it records that the bridge exists. It does not
construct that bridge.
-/
def selected_domain_final_conditional_closure_bridge_witness_statement : Prop :=
  Nonempty SelectedDomainFinalConditionalClosureBridge

/--
The unconditional construction-input witness statement.

This is a statement only: it records that the input exists. It does not
construct that input.
-/
def selected_domain_unconditional_closure_construction_input_witness_statement : Prop :=
  Nonempty SelectedDomainUnconditionalClosureConstructionInput

/--
A selected-domain construction input exists iff the final conditional closure
bridge exists, because the input is exactly a wrapper around that bridge.
-/
theorem selected_domain_unconditional_construction_input_witness_iff_final_bridge_witness :
    selected_domain_unconditional_closure_construction_input_witness_statement ↔
      selected_domain_final_conditional_closure_bridge_witness_statement := by
  constructor
  · intro h
    cases h with
    | intro input =>
        exact ⟨input.final_conditional_closure_bridge⟩
  · intro h
    cases h with
    | intro bridge =>
        exact ⟨{ final_conditional_closure_bridge := bridge }⟩

/--
A final conditional closure bridge exists iff the semantic-prefix target exists,
because the defect-atoms constructor target has already been constructed.
-/
theorem selected_domain_final_bridge_witness_iff_semantic_prefix_witness :
    selected_domain_final_conditional_closure_bridge_witness_statement ↔
      selected_domain_semantic_prefix_witness_statement := by
  constructor
  · intro h
    cases h with
    | intro bridge =>
        exact ⟨bridge.semantic_prefix⟩
  · intro h
    cases h with
    | intro semanticPrefix =>
        exact
          ⟨{ semantic_prefix := semanticPrefix
             defect_atoms_target := defect_atoms_constructor_target }⟩

/--
Therefore the current weakest selected-domain construction-input witness is
equivalent to the semantic-prefix witness.
-/
theorem selected_domain_unconditional_construction_input_witness_iff_semantic_prefix_witness :
    selected_domain_unconditional_closure_construction_input_witness_statement ↔
      selected_domain_semantic_prefix_witness_statement := by
  exact
    Iff.trans
      selected_domain_unconditional_construction_input_witness_iff_final_bridge_witness
      selected_domain_final_bridge_witness_iff_semantic_prefix_witness

end Frontier
end Chronos
