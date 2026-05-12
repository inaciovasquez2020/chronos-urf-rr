#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "Chronos/Frontier/NativeRankRateGapMissingBridge.lean"
artifact = ROOT / "artifacts/chronos/native_rank_rate_gap_missing_bridge_2026_05_12.json"
doc = ROOT / "docs/status/CHRONOS_NATIVE_RANK_RATE_GAP_MISSING_BRIDGE_2026_05_12.md"
root = ROOT / "Chronos.lean"

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "def NativeRankRateToFiberEntropyBridge : Prop :=",
    "theorem chronos_native_rank_rate_gap_iff_missing_bridge",
    "theorem chronos_native_rank_rate_gap_from_missing_bridge",
    "theorem missing_bridge_from_chronos_native_rank_rate_gap",
    "NativeRankRateGapMissingBridgeOnly",
    "nativeRankRateGapMissingBridgeBoundary",
]

for token in required_lean:
    assert token in lean_text, token

assert "import Chronos.Frontier.NativeRankRateGapMissingBridge" in root.read_text()

assert data["status"] == "FRONTIER_OPEN / WEAKEST_MISSING_BRIDGE_ONLY"
assert data["weakest_missing_object"] == "NativeRankRateToFiberEntropyBridge"
assert data["equivalence"] == "ChronosNativeRankRateGapTheorem iff NativeRankRateToFiberEntropyBridge"

for forbidden in [
    "NativeRankRateToFiberEntropyBridge proof",
    "unconditional ChronosNativeRankRateGapTheorem",
    "CountingFiberSeparation",
    "FiberMassBalance",
    "UniversalFiberEntropyGap",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "Clay-problem closure",
]:
    assert forbidden in data["does_not_assert"], forbidden
    assert forbidden in doc_text, forbidden

print("Native RankRateGap missing bridge verified.")
