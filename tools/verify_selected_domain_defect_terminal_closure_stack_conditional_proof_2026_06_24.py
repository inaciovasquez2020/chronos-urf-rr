#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/external_validation/selected_domain_defect_terminal_closure_stack_conditional_proof_2026_06_24.json"
DOC = ROOT / "docs/status/SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_STACK_CONDITIONAL_PROOF_2026_06_24.md"
LEAN = ROOT / "lean/Chronos/Frontier/SelectedDomainDefectTerminalClosureStack.lean"

data = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert data["target"] == "SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_STACK_CONDITIONAL_PROOF_2026_06_24"
assert data["status"] == "conditional_stack_proved_from_explicit_assumptions"
assert data["assumption_package"] == "SelectedDomainDefectTerminalClosureStackAssumptions"
assert data["verifier_token"] == "SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_STACK_CONDITIONAL_PROOF_2026_06_24_OK"

assert "structure SelectedDomainDefectTerminalClosureStackAssumptions : Type where" in lean
assert "theorem repair_descent_theorem" in lean
assert "theorem zero_defect_selected_domain_reentry" in lean
assert "theorem unrestricted_terminal_normalization" in lean
assert "theorem final_closure" in lean
assert "theorem unrestricted_oblivion_atom_closure" in lean
assert "CONDITIONAL_STACK_PROOF_FROM_EXPLICIT_ASSUMPTIONS" in lean

assert data["proved_theorems"] == [
    "repair_descent_theorem",
    "zero_defect_selected_domain_reentry",
    "unrestricted_terminal_normalization",
    "final_closure",
    "unrestricted_oblivion_atom_closure",
]

assert "repair_descent_theorem" in doc
assert "zero_defect_selected_domain_reentry" in doc
assert "unrestricted_terminal_normalization" in doc
assert "final_closure" in doc
assert "unrestricted_oblivion_atom_closure" in doc

assert "repair_descent_theorem -> zero_defect_selected_domain_reentry" in doc
assert "zero_defect_selected_domain_reentry -> unrestricted_terminal_normalization" in doc
assert "unrestricted_terminal_normalization -> final_closure" in doc
assert "final_closure -> unrestricted_oblivion_atom_closure" in doc

assert "BOUNDARY := conditional_on_SelectedDomainDefectTerminalClosureStackAssumptions" in doc
assert "BOUNDARY := not semantic_assumptions_constructed" in doc
assert "BOUNDARY := not defect_atoms_constructed" in doc
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in doc

assert "semantic assumptions constructed" in doc
assert "defect_atoms" in doc
assert "unconditional repair descent theorem proved" in doc
assert "unconditional zero-defect reentry theorem proved" in doc
assert "unconditional unrestricted terminal normalization proved" in doc
assert "unconditional final closure proved" in doc
assert "unconditional unrestricted Oblivion Atom closure solved" in doc

assert "SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_STACK_CONDITIONAL_PROOF_2026_06_24_OK" in doc

print("SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_STACK_CONDITIONAL_PROOF_2026_06_24_OK")
