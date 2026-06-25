#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
ARTIFACT = Path("artifacts/external_validation/selected_domain_unconditional_construction_input_witness_missing_2026_06_25.json")
DOC = Path("docs/status/SELECTED_DOMAIN_UNCONDITIONAL_CONSTRUCTION_INPUT_WITNESS_MISSING_2026_06_25.md")
artifact = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()
assert artifact["id"] == "SELECTED_DOMAIN_UNCONDITIONAL_CONSTRUCTION_INPUT_WITNESS_MISSING_2026_06_25"
assert artifact["target_branch"] == "docs/selected-domain-defect-basis-2026-06-24"
assert artifact["base_head"] == "453d3fdd"
assert artifact["status"] == "blocked_missing_nullary_unconditional_construction_input_witness"
assert artifact["failed_candidate"] == "selected_domain_unconditional_closure_constructor_obligation_matrix_constructed"
assert artifact["weakest_missing_object"] == "selected_domain_unconditional_closure_construction_input_witness"
assert "nullary witness for SelectedDomainUnconditionalClosureConstructionInput" in artifact["missing_objects"]
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in artifact["preserved_boundaries"]
branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
head = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
assert branch == artifact["target_branch"]
assert head == artifact["base_head"]
assert "SELECTED_DOMAIN_UNCONDITIONAL_CONSTRUCTION_INPUT_WITNESS_MISSING_2026_06_25_OK" in doc
assert "selected_domain_unconditional_closure_construction_input_witness" in doc
assert "BOUNDARY := not selected_domain_unconditional_closure_construction_input_witness" in doc
assert "BOUNDARY := not selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in doc
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in doc
assert "input : SelectedDomainUnconditionalClosureConstructionInput" in doc
print("SELECTED_DOMAIN_UNCONDITIONAL_CONSTRUCTION_INPUT_WITNESS_MISSING_2026_06_25_OK")
