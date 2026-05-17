#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean_path = root / "lean/Chronos/Frontier/RankRateToLyapunovExpansionFrontier.lean"
artifact_path = root / "artifacts/chronos/rank_rate_to_lyapunov_expansion_frontier_2026_05_17.json"
status_path = root / "docs/status/RANK_RATE_TO_LYAPUNOV_EXPANSION_FRONTIER_2026_05_17.md"

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
    "RankRateControlsFiberExpansion",
    "FiberExpansionControlsLyapunovSum",
    "RankRateToLyapunovExpansion",
    "rankRateToLyapunovExpansion_from_fiber_expansion",
    "MissingTheoremTarget"
]:
    assert token in lean, token

for token in [
    "Status: FRONTIER_OPEN",
    "Theorem target",
    "RankRateToLyapunovExpansion",
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
    "RankRateToLyapunovExpansion",
    "no proof of RankRateToLyapunovExpansion",
    "no unrestricted UniversalFiberEntropyGap"
]:
    assert token in artifact_text, token

forbidden = [
    "RankRateToLyapunovExpansion is proved",
    "proves RankRateToLyapunovExpansion",
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

print("RankRateToLyapunovExpansion frontier verified.")
