#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean_path = root / "lean/Chronos/Frontier/FiberEntropyMassLowerBoundsUnstableEntropyFrontier.lean"
artifact_path = root / "artifacts/chronos/fiber_entropy_mass_lower_bounds_unstable_entropy_frontier_2026_05_17.json"
status_path = root / "docs/status/FIBER_ENTROPY_MASS_LOWER_BOUNDS_UNSTABLE_ENTROPY_FRONTIER_2026_05_17.md"

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
    "FiberEntropyMassDominatesEntropyProducingPartition",
    "EntropyProducingPartitionDominatesUnstableEntropy",
    "FiberEntropyMassLowerBoundsUnstableEntropy",
    "fiberEntropyMassLowerBoundsUnstableEntropy_from_partition_dominance",
    "MissingTheoremTarget"
]:
    assert token in lean, token

for token in [
    "Status: FRONTIER_OPEN",
    "Theorem target",
    "FiberEntropyMassLowerBoundsUnstableEntropy",
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
    "FiberEntropyMassLowerBoundsUnstableEntropy",
    "no proof of FiberEntropyMassLowerBoundsUnstableEntropy",
    "no unrestricted UniversalFiberEntropyGap"
]:
    assert token in artifact_text, token

forbidden = [
    "FiberEntropyMassLowerBoundsUnstableEntropy is proved",
    "proves FiberEntropyMassLowerBoundsUnstableEntropy",
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

print("FiberEntropyMassLowerBoundsUnstableEntropy frontier verified.")
