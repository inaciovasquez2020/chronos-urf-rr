#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean_path = root / "lean/Chronos/Frontier/RateThickFiberEntropyRouteFrontierIndex.lean"
artifact_path = root / "artifacts/chronos/rate_thick_fiber_entropy_route_frontier_index_2026_05_17.json"
status_path = root / "docs/status/RATE_THICK_FIBER_ENTROPY_ROUTE_FRONTIER_INDEX_2026_05_17.md"

for path in (lean_path, artifact_path, status_path):
    assert path.exists(), f"missing required file: {path}"

lean = lean_path.read_text()
artifact_text = artifact_path.read_text()
status = status_path.read_text()
artifact = json.loads(artifact_text)

assert artifact["status"] == "FRONTIER_OPEN"
assert artifact["classification"] == "route_index_only"

for token in [
    "DimensionRegularFiberGrowthFrontier",
    "RankRateToLyapunovExpansionFrontier",
    "FiberEntropyMassLowerBoundsUnstableEntropyFrontier",
    "RateThickPositiveEntropyLowerBoundFrontier",
    "RateThickFiberEntropyRouteInputs",
    "RateThickFiberEntropyRouteFrontierIndex",
    "rateThickFiberEntropyRouteFrontierIndex_from_inputs"
]:
    assert token in lean, token

for token in [
    "Status: FRONTIER_OPEN",
    "Route inputs",
    "DimensionRegularFiberGrowth",
    "RankRateToLyapunovExpansion",
    "FiberEntropyMassLowerBoundsUnstableEntropy",
    "RateThickPositiveEntropyLowerBound",
    "route-index surface only",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem"
]:
    assert token in status, token

for token in artifact["route_inputs"]:
    assert token in artifact_text, token

forbidden = [
    "proves DimensionRegularFiberGrowth",
    "proves RankRateToLyapunovExpansion",
    "proves FiberEntropyMassLowerBoundsUnstableEntropy",
    "proves RateThickPositiveEntropyLowerBound",
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

print("Rate-thick fiber entropy route frontier index verified.")
