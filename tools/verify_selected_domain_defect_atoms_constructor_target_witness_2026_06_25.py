#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path("artifacts/external_validation/selected_domain_defect_atoms_constructor_target_witness_2026_06_25.json")
DOC = Path("docs/status/SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_TARGET_WITNESS_2026_06_25.md")
LEAN = Path("lean/Chronos/Frontier/SelectedDomainDefectAtomsConstructorTargetWitness.lean")

artifact = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert artifact["id"] == "SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_TARGET_WITNESS_2026_06_25"
assert artifact["target_branch"] == "docs/selected-domain-defect-basis-2026-06-24"

assert "SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_TARGET_WITNESS_2026_06_25_OK" in doc
assert "def defect_atoms_constructor_target" in lean
assert "SelectedDomainDefectAtomsConstructionTarget" in lean
assert "BOUNDARY := not selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in doc

for token in [
    "defect_atoms_construction_statement := True",
    "terminal_cardinality_defect_statement := True",
    "selected_domain_reentry_defect_statement := True",
    "repair_step_compatibility_defect_statement := True",
    "normalization_transfer_defect_statement := True",
]:
    assert token in lean

for forbidden in ["axiom ", "opaque ", "sorry", "admit"]:
    assert forbidden not in lean

print("SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_TARGET_WITNESS_2026_06_25_OK")
