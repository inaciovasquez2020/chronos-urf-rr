#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/qk_dini_uniform_coefficient_bounds_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/QKDiniUniformCoefficientBounds.lean"
status_doc = ROOT / "docs/status/QKDINI_UNIFORM_COEFFICIENT_BOUNDS_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())

assert data["object"] == "QKDiniUniformCoefficientBounds"
assert data["status"] == "UNIFORM_COEFFICIENT_BOUNDS_INTERFACE_ONLY"
assert data["minimal_missing_object"] == "ConcreteQKDiniCoefficientFamilyBoundWitness"

lean_text = lean_file.read_text()
assert "structure QKDiniUniformCoefficientBounds" in lean_text
assert "theorem qkDiniUniformCoefficientBounds_boundary" in lean_text
assert "axiom " not in lean_text
assert "sorry" not in lean_text

status_text = status_doc.read_text()
assert "NO_FINAL_THEOREM_CLOSURE" in " ".join(data["boundary"])
assert "no final theorem closure" in status_text.lower()

assert "import Chronos.Frontier.QKDiniUniformCoefficientBounds" in root_import.read_text()

print("QKDINI_UNIFORM_COEFFICIENT_BOUNDS_OK")
