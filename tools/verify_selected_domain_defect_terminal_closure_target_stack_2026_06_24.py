#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/external_validation/selected_domain_defect_terminal_closure_target_stack_2026_06_24.json"
DOC = ROOT / "docs/status/SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_TARGET_STACK_2026_06_24.md"
PRIOR = ROOT / "artifacts/external_validation/selected_domain_defect_repair_interface_schema_2026_06_24.json"

data = json.loads(ARTIFACT.read_text())
prior = json.loads(PRIOR.read_text())
doc = DOC.read_text()

assert prior["target"] == "SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_SCHEMA_2026_06_24"
assert data["target"] == "SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_TARGET_STACK_2026_06_24"
assert data["status"] == "requested_terminal_closure_stack_recorded_not_proved"
assert data["depends_on"] == prior["target"]
assert data["verifier_token"] == "SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_TARGET_STACK_2026_06_24_OK"

expected_stack = [
    "repair_descent_theorem",
    "zero_defect_selected_domain_reentry",
    "unrestricted_terminal_normalization",
    "final_closure",
]

actual_stack = [item["target"] for item in data["requested_stack"]]
assert actual_stack == expected_stack
assert data["formal_statement_targets"] == expected_stack
assert [item["order"] for item in data["requested_stack"]] == [1, 2, 3, 4]

assert data["dependency_edges"] == [
    "repair_descent_theorem -> zero_defect_selected_domain_reentry",
    "zero_defect_selected_domain_reentry -> unrestricted_terminal_normalization",
    "unrestricted_terminal_normalization -> final_closure",
]

assert data["allowed_next_formalization"] == [
    "create statement surface for repair_descent_theorem",
    "create statement surface for zero_defect_selected_domain_reentry",
    "create statement surface for unrestricted_terminal_normalization",
    "create statement surface for final_closure",
]

assert "BOUNDARY := not repair_descent_theorem_proved" in data["boundary"]
assert "BOUNDARY := not zero_defect_selected_domain_reentry_proved" in data["boundary"]
assert "BOUNDARY := not unrestricted_terminal_normalization_proved" in data["boundary"]
assert "BOUNDARY := not final_closure_proved" in data["boundary"]
assert "BOUNDARY := not unrestricted_oblivion_atom_closure_solved" in data["boundary"]

assert "repair_descent_theorem proved" in data["not_claimed"]
assert "zero_defect_selected_domain_reentry proved" in data["not_claimed"]
assert "unrestricted_terminal_normalization proved" in data["not_claimed"]
assert "final_closure proved" in data["not_claimed"]
assert "unrestricted Oblivion Atom closure solved" in data["not_claimed"]

assert "repair_descent_theorem" in doc
assert "zero_defect_selected_domain_reentry" in doc
assert "unrestricted_terminal_normalization" in doc
assert "final_closure" in doc

assert "repair_descent_theorem -> zero_defect_selected_domain_reentry" in doc
assert "zero_defect_selected_domain_reentry -> unrestricted_terminal_normalization" in doc
assert "unrestricted_terminal_normalization -> final_closure" in doc

assert "BOUNDARY := not repair_descent_theorem_proved" in doc
assert "BOUNDARY := not zero_defect_selected_domain_reentry_proved" in doc
assert "BOUNDARY := not unrestricted_terminal_normalization_proved" in doc
assert "BOUNDARY := not final_closure_proved" in doc
assert "BOUNDARY := not unrestricted_oblivion_atom_closure_solved" in doc

assert "SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_TARGET_STACK_2026_06_24_OK" in doc

print("SELECTED_DOMAIN_DEFECT_TERMINAL_CLOSURE_TARGET_STACK_2026_06_24_OK")
