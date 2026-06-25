#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ARTIFACT = Path("artifacts/external_validation/selected_domain_construction_input_witness_reduction_statement_2026_06_25.json")
DOC = Path("docs/status/SELECTED_DOMAIN_CONSTRUCTION_INPUT_WITNESS_REDUCTION_STATEMENT_2026_06_25.md")
LEAN = Path("lean/Chronos/Frontier/SelectedDomainConstructionInputWitnessReductionStatement.lean")

artifact = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert artifact["id"] == "SELECTED_DOMAIN_CONSTRUCTION_INPUT_WITNESS_REDUCTION_STATEMENT_2026_06_25"
assert artifact["target_branch"] == "docs/selected-domain-defect-basis-2026-06-24"
assert artifact["base_head"] == "1fbefc8a"
assert artifact["lean_target"] == "Chronos.Frontier.SelectedDomainConstructionInputWitnessReductionStatement"
assert artifact["available_constructed_component"] == "defect_atoms_constructor_target"
assert artifact["weakest_missing_object_after_reduction"] == "selected_domain_semantic_prefix_witness"
assert artifact["status"] == "selected_domain_construction_input_witness_reduced_to_semantic_prefix_witness"

required_boundaries = [
    "BOUNDARY := not selected_domain_semantic_prefix_witness",
    "BOUNDARY := not selected_domain_unconditional_closure_construction_input_witness",
    "BOUNDARY := not selected_domain_unconditional_closure_constructor_obligation_matrix_constructed",
    "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved",
]

for boundary in required_boundaries:
    assert boundary in artifact["preserved_boundaries"]
    assert boundary in doc

required_lean_tokens = [
    "def selected_domain_semantic_prefix_witness_statement",
    "def selected_domain_final_conditional_closure_bridge_witness_statement",
    "def selected_domain_unconditional_closure_construction_input_witness_statement",
    "theorem selected_domain_unconditional_construction_input_witness_iff_final_bridge_witness",
    "theorem selected_domain_final_bridge_witness_iff_semantic_prefix_witness",
    "theorem selected_domain_unconditional_construction_input_witness_iff_semantic_prefix_witness",
    "defect_atoms_constructor_target",
]

for token in required_lean_tokens:
    assert token in lean

for forbidden in ["axiom ", "opaque ", "sorry", "admit"]:
    assert forbidden not in lean

branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
head = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
base_head = artifact["base_head"]
assert branch == artifact["target_branch"]
subprocess.run(["git", "merge-base", "--is-ancestor", base_head, head], check=True)

assert "SELECTED_DOMAIN_CONSTRUCTION_INPUT_WITNESS_REDUCTION_STATEMENT_2026_06_25_OK" in doc
assert "selected_domain_semantic_prefix_witness" in doc
assert "This layer does not construct the semantic-prefix witness" in doc

print("SELECTED_DOMAIN_CONSTRUCTION_INPUT_WITNESS_REDUCTION_STATEMENT_2026_06_25_OK")
