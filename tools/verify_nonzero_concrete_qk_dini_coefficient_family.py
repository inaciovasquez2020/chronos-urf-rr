#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/nonzero_concrete_qk_dini_coefficient_family_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/NonzeroConcreteQKDiniCoefficientFamily.lean"
status_doc = ROOT / "docs/status/NONZERO_CONCRETE_QK_DINI_COEFFICIENT_FAMILY_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
lean_text = lean_file.read_text()
status_text = status_doc.read_text()
root_text = root_import.read_text()

assert data["object"] == "NonzeroConcreteQKDiniCoefficientFamily"
assert data["status"] == "NONZERO_CONCRETE_CONSTANT_ONE_FAMILY_BOUND_WITNESS_ONLY"
assert data["coefficient_rule"] == "coefficient i n = 1"
assert data["uniform_bound"] == 1
assert data["minimal_missing_object"] == "ScientificallyDerivedQKDiniCoefficientFamily"

assert "coefficient := fun _ _ => 1" in lean_text
assert "theorem nonzeroConcreteQKDiniCoefficientFamily_nonzero" in lean_text
assert "def NonzeroConcreteQKDiniCoefficientFamilyBoundWitness" in lean_text
assert "theorem nonzeroConcreteQKDiniCoefficientFamily_uniform_bound" in lean_text
assert "axiom " not in lean_text
assert "sorry" not in lean_text

assert "NO_SCIENTIFICALLY_DERIVED_QK_DINI_COEFFICIENT_FAMILY" in data["boundary"]
assert "NO_ANALYTIC_DINI_ESTIMATE_PROOF" in data["boundary"]
assert "NO_FINAL_THEOREM_CLOSURE" in data["boundary"]
assert "NO_FINAL_SCIENTIFIC_CLOSURE" in data["boundary"]

assert "nonzero constant-one formal family only" in status_text.lower()
assert "import Chronos.Frontier.NonzeroConcreteQKDiniCoefficientFamily" in root_text

print("NONZERO_CONCRETE_QK_DINI_COEFFICIENT_FAMILY_OK")
