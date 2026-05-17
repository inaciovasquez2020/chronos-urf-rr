#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean_path = root / "lean/Chronos/Frontier/RateThickConditionalReductionOnly.lean"
artifact_path = root / "artifacts/chronos/rate_thick_conditional_reduction_only_2026_05_17.json"
status_path = root / "docs/status/RATE_THICK_CONDITIONAL_REDUCTION_ONLY_2026_05_17.md"

for path in (lean_path, artifact_path, status_path):
    assert path.exists(), f"missing required file: {path}"

lean = lean_path.read_text()
artifact_text = artifact_path.read_text()
status = status_path.read_text()
artifact = json.loads(artifact_text)

assert artifact["status"] == "CONDITIONAL_REDUCTION_ONLY"

for token in [
    "ConditionalReductionOnly",
    "DimensionRegularFiberGrowth",
    "dimensionRegularFiberGrowth_implies_rankRate_nonNullFiberWitness",
    "RankRateToLyapunovExpansion",
    "rankRateToLyapunovExpansion_implies_lyapunov_lower_bound",
    "FiberEntropyMassLowerBoundsUnstableEntropy",
    "fiberEntropyMassLowerBoundsUnstableEntropy_apply",
    "RateThickFiberEntropyGap",
    "rateThickFiberEntropyGap_from_entropy_lower_bound",
]:
    assert token in lean, token

for token in [
    "Status: CONDITIONAL_REDUCTION_ONLY",
    "conditional reduction surface only",
    "DimensionRegularFiberGrowth",
    "RankRateToLyapunovExpansion",
    "FiberEntropyMassLowerBoundsUnstableEntropy",
    "full-category fiber-entropy gap closure",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in status, token

for token in [
    "DimensionRegularFiberGrowth",
    "RankRateToLyapunovExpansion",
    "FiberEntropyMassLowerBoundsUnstableEntropy",
]:
    assert token in artifact_text, token

forbidden_parts = [
    ("unconditional", "UniversalFiberEntropyGap"),
    ("proves", "full-category fiber-entropy gap"),
    ("proves", "unrestricted Chronos-RR"),
    ("proves", "unrestricted H4.1/FGL"),
    ("proves", "P vs NP"),
    ("solves", "P vs NP"),
    ("solves", "Clay problem"),
]

combined = "\n".join([lean, artifact_text, status]).lower()
for left, right in forbidden_parts:
    assert f"{left} {right}".lower() not in combined, f"{left} {right}"

print("Rate-thick conditional reduction-only surface verified.")
