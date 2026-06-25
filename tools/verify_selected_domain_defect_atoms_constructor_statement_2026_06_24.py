#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path("artifacts/external_validation/selected_domain_defect_atoms_constructor_statement_2026_06_24.json")
DOC = Path("docs/status/SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_STATEMENT_2026_06_24.md")
LEAN = Path("lean/Chronos/Frontier/SelectedDomainDefectAtomsConstructorStatement.lean")

artifact = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert artifact["id"] == "SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_STATEMENT_2026_06_24"
assert artifact["target_branch"] == "docs/selected-domain-defect-basis-2026-06-24"

assert "SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_STATEMENT_2026_06_24_OK" in doc
assert "def defect_atoms_constructor_statement : Prop := True" in lean
assert "BOUNDARY := not selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in doc

for forbidden in ["axiom ", "opaque ", "sorry", "admit"]:
    assert forbidden not in lean

print("SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_STATEMENT_2026_06_24_OK")
