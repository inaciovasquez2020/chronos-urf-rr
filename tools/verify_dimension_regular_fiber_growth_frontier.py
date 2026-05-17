#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean_path = root / "lean/Chronos/Frontier/DimensionRegularFiberGrowthFrontier.lean"
artifact_path = root / "artifacts/chronos/dimension_regular_fiber_growth_frontier_2026_05_17.json"
status_path = root / "docs/status/DIMENSION_REGULAR_FIBER_GROWTH_FRONTIER_2026_05_17.md"

for path in (lean_path, artifact_path, status_path):
    assert path.exists(), f"missing required file: {path}"

lean = lean_path.read_text()
artifact_text = artifact_path.read_text()
status = status_path.read_text()
artifact = json.loads(artifact_text)

assert artifact["status"] == "FRONTIER_OPEN"
assert artifact["classification"] == "theorem_target_only"

for token in [
    "FRONTIER_OPEN",
    "PositiveFiberDimensionWitness",
    "DimensionRegularFiberGrowth",
    "PositiveFiberDimensionToNonNullFiberWitness",
    "DimensionRegularFiberGrowthBridge",
    "dimensionRegularFiberGrowth_to_nonNullFiberWitness",
    "MissingTheoremTarget"
]:
    assert token in lean, token

for token in [
    "Status: FRONTIER_OPEN",
    "Theorem target",
    "DimensionRegularFiberGrowth",
    "Missing theorem",
    "theorem-target surface only",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem"
]:
    assert token in status, token

for token in [
    "FRONTIER_OPEN",
    "theorem_target_only",
    "DimensionRegularFiberGrowth",
    "no proof of DimensionRegularFiberGrowth",
    "no unrestricted UniversalFiberEntropyGap"
]:
    assert token in artifact_text, token

forbidden = [
    "DimensionRegularFiberGrowth is proved",
    "proves DimensionRegularFiberGrowth",
    "proves RateThickFiberEntropyGap",
    "proves unrestricted UniversalFiberEntropyGap",
    "proves unrestricted Chronos-RR",
    "proves unrestricted H4.1/FGL",
    "proves P vs NP",
    "solves P vs NP",
    "solves a Clay problem"
]

combined = "\n".join([lean, artifact_text, status]).lower()
for token in forbidden:
    assert token.lower() not in combined, token

print("DimensionRegularFiberGrowth frontier verified.")
