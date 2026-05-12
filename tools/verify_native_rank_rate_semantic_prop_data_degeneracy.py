#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "Chronos/Frontier/NativeRankRateSemanticPropDataDegeneracy.lean"
artifact = ROOT / "artifacts/chronos/native_rank_rate_semantic_prop_data_degeneracy_2026_05_12.json"
doc = ROOT / "docs/status/CHRONOS_NATIVE_RANK_RATE_SEMANTIC_PROP_DATA_DEGENERACY_2026_05_12.md"
root = ROOT / "Chronos.lean"

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "theorem semantic_rank_rate_to_fiber_entropy_soundness_from_prop_data",
    "theorem encoded_rank_rate_certificate_soundness_from_prop_data",
    "theorem encoded_fiber_entropy_certificate_realization_from_prop_data",
    "theorem native_rank_rate_semantic_certificate_soundness_from_prop_data",
    "theorem chronos_native_rank_rate_gap_from_semantic_prop_data",
    "NativeRankRateSemanticPropDataDegeneracyOnly",
    "nativeRankRateSemanticPropDataDegeneracyBoundary",
]

for token in required_lean:
    assert token in lean_text, token

assert "import Chronos.Frontier.NativeRankRateSemanticPropDataDegeneracy" in root.read_text()
assert data["status"] == "SEMANTIC_PROP_DATA_SURFACE_ONLY"
assert data["new_missing_object"] == "non-Prop semantic invariant linking rank-rate structure to fiber-entropy structure"

for token in [
    "SemanticRankRateToFiberEntropySoundness",
    "EncodedRankRateCertificateSoundness",
    "EncodedFiberEntropyCertificateRealization",
    "NativeRankRateSemanticCertificateSoundness",
    "ChronosNativeRankRateGapTheorem",
]:
    assert token in data["proved_encoded_surface"], token

for forbidden in [
    "non-Prop semantic invariant",
    "genuine SemanticRankRateToFiberEntropySoundness",
    "semantic RankRateGap theorem",
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

print("Native RankRateGap semantic Prop-data degeneracy verified.")
