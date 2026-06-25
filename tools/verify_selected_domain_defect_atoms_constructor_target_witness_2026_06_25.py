#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
ARTIFACT = Path("artifacts/external_validation/selected_domain_defect_atoms_constructor_target_witness_2026_06_25.json")
DOC = Path("docs/status/SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_TARGET_WITNESS_2026_06_25.md")
LEAN = Path("lean/Chronos/Frontier/SelectedDomainDefectAtomsConstructorTargetWitness.lean")
artifact = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()
assert artifact["id"] == "SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_TARGET_WITNESS_2026_06_25"
assert artifact["target_branch"] == "docs/selected-domain-defect-basis-2026-06-24"
assert artifact["base_head"] == "9f172612"
assert artifact["constructed_object"] == "defect_atoms_constructor_target"
assert artifact["constructed_type"] == "SelectedDomainDefectAtomsConstructionTarget"
assert artifact["status"] == "defect_atoms_constructor_target_witness_constructed"
assert artifact["next_weakest_object"] == "selected_domain_unconditional_closure_constructor_obligation_matrix_constructed"
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in artifact["preserved_boundaries"]
assert "BOUNDARY := not selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in artifact["preserved_boundaries"]
branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
assert branch == artifact["target_branch"]
assert "def defect_atoms_constructor_target" in lean
assert "SelectedDomainDefectAtomsConstructionTarget" in lean
assert "SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_TARGET_WITNESS_2026_06_25_OK" in doc
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in doc
assert "BOUNDARY := not selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in doc
assert "does not assert unconditional unrestricted Oblivion Atom closure" in doc
print("SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTOR_TARGET_WITNESS_2026_06_25_OK")
