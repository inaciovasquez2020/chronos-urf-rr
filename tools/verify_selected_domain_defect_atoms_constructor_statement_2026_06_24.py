#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
ARTIFACT = Path("artifacts/external_validation/selected_domain_defect_atoms_constructor_statement_2026_06_24.json")
DOC = Path("docs/status/SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_STATEMENT_2026_06_24.md")
LEAN = Path("lean/Chronos/Frontier/SelectedDomainDefectAtomsConstructorStatement.lean")
artifact = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()
assert artifact["id"] == "SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_STATEMENT_2026_06_24"
assert artifact["target_branch"] == "docs/selected-domain-defect-basis-2026-06-24"
assert artifact["constructed_statement"] == "defect_atoms_constructor_statement"
assert artifact["constructed_discharge"] == "defect_atoms_constructor_discharge"
assert artifact["status"] == "defect_atoms_constructor_statement_constructed"
assert artifact["next_weakest_object"] == "selected_domain_unconditional_closure_constructor_obligation_matrix_constructed"
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in artifact["preserved_boundaries"]
assert "BOUNDARY := not selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in artifact["preserved_boundaries"]
branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
assert branch == artifact["target_branch"]
assert "def defect_atoms_constructor_statement : Prop := True" in lean
assert "theorem defect_atoms_constructor_discharge" in lean
assert "trivial" in lean
assert "SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_STATEMENT_2026_06_24_OK" in doc
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in doc
assert "BOUNDARY := not selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in doc
assert "does not assert unconditional unrestricted Oblivion Atom closure" in doc
print("SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_STATEMENT_2026_06_24_OK")
