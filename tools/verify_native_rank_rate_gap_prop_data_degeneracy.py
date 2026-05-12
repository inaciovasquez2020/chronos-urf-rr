#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "Chronos/Frontier/NativeRankRateGapPropDataDegeneracy.lean"
artifact = ROOT / "artifacts/chronos/native_rank_rate_gap_prop_data_degeneracy_2026_05_12.json"
doc = ROOT / "docs/status/CHRONOS_NATIVE_RANK_RATE_GAP_PROP_DATA_DEGENERACY_2026_05_12.md"
root = ROOT / "Chronos.lean"

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "theorem native_rank_rate_to_fiber_entropy_bridge_from_prop_data",
    "theorem chronos_native_rank_rate_gap_from_prop_data",
    "NativeRankRateGapPropDataDegeneracyOnly",
    "nativeRankRateGapPropDataDegeneracyBoundary",
    "exact ⟨hRank.rankRateCertificate⟩",
]

for token in required_lean:
    assert token in lean_text, token

assert "import Chronos.Frontier.NativeRankRateGapPropDataDegeneracy" in root.read_text()
assert data["status"] == "ENCODED_PROP_DATA_SURFACE_ONLY"
assert data["new_missing_object"] == "semantic certificate soundness tying rank-rate certificates to fiber-entropy certificates"

for forbidden in [
    "semantic NativeRankRateToFiberEntropyBridge",
    "semantic RankRateGap",
    "CountingFiberSeparation",
    "FiberMassBalance",
    "UniversalFiberEntropyGap",
    "broader DepthBridge",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "Clay-problem closure",
]:
    assert forbidden in data["does_not_assert"], forbidden
    assert forbidden in doc_text, forbidden

print("Native RankRateGap prop-data degeneracy verified.")
