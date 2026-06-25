#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/external_validation/selected_domain_defect_terminal_closure_assumption_discharge_2026_06_24.json"
DOC = ROOT / "docs/status/SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_ASSUMPTION_DISCHARGE_2026_06_24.md"
LEAN = ROOT / "lean/Chronos/Frontier/SelectedDomainDefectTerminalClosureAssumptionDischarge.lean"

data = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert data["target"] == "SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_ASSUMPTION_DISCHARGE_2026_06_24"
assert data["status"] == "component_discharge_constructs_stack_assumptions"
assert data["component_package"] == "SelectedDomainDefectTerminalClosureComponentDischarge"
assert data["constructed_package"] == "SelectedDomainDefectTerminalClosureStackAssumptions"
assert data["constructor"] == "terminal_closure_stack_assumptions_from_component_discharge"
assert data["verifier_token"] == "SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_ASSUMPTION_DISCHARGE_2026_06_24_OK"

assert "import Chronos.Frontier.SelectedDomainDefectTerminalClosureStack" in lean
assert "structure SelectedDomainDefectTerminalClosureComponentDischarge : Type where" in lean
assert "def terminal_closure_stack_assumptions_from_component_discharge" in lean
assert "SelectedDomainDefectTerminalClosureStackAssumptions" in lean
assert "COMPONENT_DISCHARGE_PACKAGE_TO_CONDITIONAL_STACK_ASSUMPTIONS" in lean

assert "repair_descent_theorem_from_component_discharge" in lean
assert "zero_defect_selected_domain_reentry_from_component_discharge" in lean
assert "unrestricted_terminal_normalization_from_component_discharge" in lean
assert "final_closure_from_component_discharge" in lean
assert "unrestricted_oblivion_atom_closure_from_component_discharge" in lean

assert "repair_descent_theorem_from_component_discharge" in doc
assert "zero_defect_selected_domain_reentry_from_component_discharge" in doc
assert "unrestricted_terminal_normalization_from_component_discharge" in doc
assert "final_closure_from_component_discharge" in doc
assert "unrestricted_oblivion_atom_closure_from_component_discharge" in doc

assert "repair_descent_discharge" in lean
assert "zero_defect_selected_domain_reentry_discharge" in lean
assert "unrestricted_terminal_normalization_discharge" in lean
assert "final_closure_discharge" in lean
assert "unrestricted_oblivion_atom_closure_discharge" in lean

assert "repair_descent_discharge" in doc
assert "zero_defect_selected_domain_reentry_discharge" in doc
assert "unrestricted_terminal_normalization_discharge" in doc
assert "final_closure_discharge" in doc
assert "unrestricted_oblivion_atom_closure_discharge" in doc

assert "BOUNDARY := conditional_on_SelectedDomainDefectTerminalClosureComponentDischarge" in doc
assert "BOUNDARY := not semantic_component_discharges_constructed" in doc
assert "BOUNDARY := not defect_atoms_constructed" in doc
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in doc

assert "semantic component discharges constructed" in doc
assert "defect_atoms" in doc
assert "unconditional unrestricted Oblivion Atom closure solved" in doc

assert "SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_ASSUMPTION_DISCHARGE_2026_06_24_OK" in doc

print("SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_ASSUMPTION_DISCHARGE_2026_06_24_OK")
