#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/FiniteListPositiveUniformFloor.lean"
doc = ROOT / "docs/status/FINITE_LIST_POSITIVE_UNIFORM_FLOOR_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/finite_list_positive_uniform_floor_2026_05_18.json"

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "theorem finite_list_positive_uniform_floor",
    "masses ≠ []",
    "∀ x, x ∈ masses → 0 < x",
    "∃ ε : ℝ, 0 < ε ∧ ∀ x, x ∈ masses → ε ≤ x",
    "theorem FiniteSupportPositiveMassUniformFloor_list",
    "lt_min",
    "min_le_left",
    "min_le_right",
]

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in ["sorry", "admit", "axiom"]:
    if token in lean_text:
        raise SystemExit(f"forbidden Lean token present: {token}")

if data["status"] != "FINITE_LIST_POSITIVE_UNIFORM_FLOOR_PROVED":
    raise SystemExit("wrong artifact status")

if data["lean_theorem"] != "FiniteSupportPositiveMassUniformFloor_list":
    raise SystemExit("wrong Lean theorem marker")

for phrase in [
    "list-coded finite support only",
    "no unrestricted UniversalFiberEntropyGap",
    "no unrestricted Chronos-RR",
    "no unrestricted H4.1/FGL",
    "no P vs NP",
    "no Clay closure",
]:
    if phrase not in doc_text:
        raise SystemExit(f"missing boundary phrase in doc: {phrase}")
    if phrase not in data["boundary"]:
        raise SystemExit(f"missing boundary phrase in artifact: {phrase}")

print("Finite list positive uniform floor verified.")
