#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "Chronos/Frontier/NativeRankRateSemanticCertificateSoundness.lean"
artifact = ROOT / "artifacts/chronos/native_rank_rate_semantic_certificate_soundness_2026_05_12.json"
doc = ROOT / "docs/status/CHRONOS_NATIVE_RANK_RATE_SEMANTIC_CERTIFICATE_SOUNDNESS_2026_05_12.md"
root = ROOT / "Chronos.lean"

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "structure SemanticRankRateCertificate",
    "structure SemanticFiberEntropyCertificate",
    "def EncodedRankRateCertificateSoundness : Prop :=",
    "def EncodedFiberEntropyCertificateRealization : Prop :=",
    "def SemanticRankRateToFiberEntropySoundness : Prop :=",
    "structure NativeRankRateSemanticCertificateSoundness : Prop where",
    "theorem native_rank_rate_to_fiber_entropy_bridge_from_semantic_soundness",
    "theorem chronos_native_rank_rate_gap_from_semantic_soundness",
    "NativeRankRateSemanticCertificateSoundnessOnly",
    "nativeRankRateSemanticCertificateSoundnessBoundary",
]

for token in required_lean:
    assert token in lean_text, token

assert "import Chronos.Frontier.NativeRankRateSemanticCertificateSoundness" in root.read_text()
assert data["status"] == "FRONTIER_OPEN / SEMANTIC_CERTIFICATE_SOUNDNESS_INTERFACE_ONLY"
assert data["weakest_missing_object"] == "SemanticRankRateToFiberEntropySoundness"

for token in [
    "EncodedRankRateCertificateSoundness",
    "SemanticRankRateToFiberEntropySoundness",
    "EncodedFiberEntropyCertificateRealization",
]:
    assert token in data["sufficient_package"], token
    assert token in doc_text, token

for token in [
    "NativeRankRateToFiberEntropyBridge",
    "ChronosNativeRankRateGapTheorem",
]:
    assert token in data["derives_encoded_surface"], token

for forbidden in [
    "SemanticRankRateToFiberEntropySoundness proof",
    "semantic RankRateGap proof",
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

print("Native RankRateGap semantic certificate soundness verified.")
