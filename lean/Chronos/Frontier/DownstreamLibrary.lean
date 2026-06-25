import Chronos.Frontier.SelectedDomainSemanticPrefixWitness

namespace Chronos
namespace Frontier

/--
Stable downstream wrapper for the selected-domain semantic-prefix witness.
-/
theorem downstream_selected_domain_semantic_prefix_witness :
    selected_domain_semantic_prefix_witness_statement :=
  selected_domain_semantic_prefix_witness_statement_discharge

/--
Stable downstream wrapper for the selected-domain unconditional construction
input witness.
-/
theorem downstream_selected_domain_unconditional_closure_construction_input_witness :
    selected_domain_unconditional_closure_construction_input_witness_statement :=
  selected_domain_unconditional_closure_construction_input_witness_discharge

/--
Stable downstream wrapper for the selected-domain final conditional closure
bridge witness.
-/
theorem downstream_selected_domain_final_conditional_closure_bridge_witness :
    selected_domain_final_conditional_closure_bridge_witness_statement :=
  selected_domain_final_conditional_closure_bridge_witness_discharge

end Frontier
end Chronos
