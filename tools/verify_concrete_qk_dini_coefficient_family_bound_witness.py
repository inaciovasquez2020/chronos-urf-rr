#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/concrete_qk_dini_coefficient_family_bound_witness_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/ConcreteQKDiniCoefficientFamilyBoundWitness.lean"
status_doc = ROOT / "docs/status/CONCRETE_QK_DINI_COEFFICIENT_FAMILY_BOUND_WITNESS_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
lean_text = lean_file.read_text()
status_text = status_doc.read_text()
root_text = root_import.read_text()

assert data["object"] == "ConcreteQKDiniCoefficientFamilyBoundWitness"
assert data["status"] == "CONCRETE_ZERO_FAMILY_BOUND_WITNESS_ONLY"
assert data["minimal_missing_object"] == "NonzeroOrScientificallyDerivedQKDiniCoefficientFamily"

assert "def ConcreteQKDiniCoefficientFamily" in lean_text
assert "def ConcreteQKDiniCoefficientFamilyBoundWitness" in lean_text
assert "theorem concreteQKDiniCoefficientFamilyBoundWitness_closed" in lean_text
assert "coefficient := fun _ _ => 0" in lean_text
assert "axiom " not in lean_text
assert "sorry" not in lean_text

assert "NO_FINAL_THEOREM_CLOSURE" in data["boundary"]
assert "NO_FINAL_SCIENTIFIC_CLOSURE" in data["boundary"]
assert "concrete zero-family witness only" in status_text.lower()
assert "import Chronos.Frontier.ConcreteQKDiniCoefficientFamilyBoundWitness" in root_text

print("CONCRETE_QK_DINI_COEFFICIENT_FAMILY_BOUND_WITNESS_OK")
