import Chronos.Frontier.SelectedDomainUnconditionalClosureConstructorObligationMatrix

namespace Chronos
namespace Frontier

/--
Construct a `SelectedDomainUnconditionalClosureConstructorObligationMatrix`
from a `SelectedDomainUnconditionalClosureConstructionInput`.

Both constructor statements are `True`; both discharges are `trivial`; both
target functions ignore the proof and project from the final conditional
closure bridge carried by the input.

Boundary: constructs the obligation matrix from the input; does not construct
the input and does not prove unconditional unrestricted Oblivion Atom closure.
-/
def selected_domain_unconditional_closure_constructor_obligation_matrix_from_construction_input
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    SelectedDomainUnconditionalClosureConstructorObligationMatrix :=
  { semantic_prefix_constructor_statement := True
    semantic_prefix_constructor_discharge := trivial
    semantic_prefix_constructor_target :=
      fun _ => input.final_conditional_closure_bridge.semantic_prefix
    defect_atoms_constructor_statement := True
    defect_atoms_constructor_discharge := trivial
    defect_atoms_constructor_target :=
      fun _ => input.final_conditional_closure_bridge.defect_atoms_target }

/--
The semantic-prefix round-trip: applying the target to the discharge returns
the bridge's semantic prefix. Proved by `rfl`.
-/
theorem semantic_prefix_witness_round_trips
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    semantic_prefix_constructor_target_from_obligation_matrix
      (selected_domain_unconditional_closure_constructor_obligation_matrix_from_construction_input
        input) =
    input.final_conditional_closure_bridge.semantic_prefix :=
  rfl

/--
The defect-atoms round-trip: applying the target to the discharge returns the
bridge's defect-atoms target. Proved by `rfl`.
-/
theorem defect_atoms_witness_round_trips
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    defect_atoms_constructor_target_from_obligation_matrix
      (selected_domain_unconditional_closure_constructor_obligation_matrix_from_construction_input
        input) =
    input.final_conditional_closure_bridge.defect_atoms_target :=
  rfl

end Frontier
end Chronos
