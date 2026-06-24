import Chronos.Frontier.SelectedDomainUnconditionalClosureConstructorTarget

namespace Chronos
namespace Frontier

/--
A named solved-target surface for unrestricted Oblivion Atom closure obtained
from a constructor target.

Boundary: this is not an unconditional construction of the constructor target.
It packages the final theorem surface once the constructor target is supplied.
-/
structure SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget : Type where
  constructor_target :
    SelectedDomainUnconditionalClosureConstructorTarget

/--
Extract the constructor target from the solved-target surface.
-/
def selected_domain_constructor_target_from_unconditional_solved_surface
    (surface :
      SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget) :
    SelectedDomainUnconditionalClosureConstructorTarget :=
  surface.constructor_target

/--
Build the already named unconditional closure construction input from the
solved-target surface.
-/
def selected_domain_unconditional_closure_construction_input_from_solved_surface
    (surface :
      SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget) :
    SelectedDomainUnconditionalClosureConstructionInput :=
  selected_domain_unconditional_closure_construction_input_from_constructor_target
    surface.constructor_target

/--
Expose the final conditional bridge from the solved-target surface.
-/
def selected_domain_final_conditional_closure_bridge_from_solved_surface
    (surface :
      SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget) :
    SelectedDomainFinalConditionalClosureBridge :=
  selected_domain_final_conditional_closure_bridge_from_constructor_target
    surface.constructor_target

/--
Expose the semantic component bundle from the solved-target surface.
-/
def selected_domain_semantic_component_targets_from_solved_surface
    (surface :
      SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget) :
    SelectedDomainDefectSemanticComponentTargets :=
  selected_domain_semantic_component_targets_from_constructor_target
    surface.constructor_target

/--
Expose the defect-atoms construction target from the solved-target surface.
-/
def selected_domain_defect_atoms_target_from_solved_surface
    (surface :
      SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget) :
    SelectedDomainDefectAtomsConstructionTarget :=
  selected_domain_defect_atoms_target_from_unconditional_closure_constructor_target
    surface.constructor_target

/--
The defect-atoms construction statement follows from the solved-target surface.
-/
theorem defect_atoms_construction_statement_from_solved_surface
    (surface :
      SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget) :
    (selected_domain_defect_atoms_target_from_solved_surface
      surface).defect_atoms_construction_statement :=
  defect_atoms_construction_statement_from_constructor_target
    surface.constructor_target

/--
The unrestricted Oblivion Atom closure statement follows from the solved-target
surface by using the constructor-target bridge.

Boundary: this remains conditional on an inhabitant of
`SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget`.
It does not construct that inhabitant.
-/
theorem unrestricted_oblivion_atom_closure_statement_from_solved_surface
    (surface :
      SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      (selected_domain_semantic_component_targets_from_solved_surface
        surface)).unrestricted_oblivion_atom_closure_statement :=
  unrestricted_oblivion_atom_closure_statement_from_constructor_target
    surface.constructor_target

/--
A boundary theorem surface: if the solved-target surface is supplied, then the
current selected-domain closure theorem surface is available.

This is the strongest admissible bridge here without constructing the
constructor target.
-/
theorem selected_domain_unconditional_unrestricted_oblivion_atom_closure_solved_if_constructor_target_constructed
    (surface :
      SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      (selected_domain_semantic_component_targets_from_solved_surface
        surface)).unrestricted_oblivion_atom_closure_statement :=
  unrestricted_oblivion_atom_closure_statement_from_solved_surface
    surface

end Frontier
end Chronos
