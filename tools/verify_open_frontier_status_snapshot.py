#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/status/CHRONOS_OPEN_FRONTIER_STATUS_SNAPSHOT_2026_05_09.md"
ART = ROOT / "artifacts/chronos/open_frontier_status_snapshot_2026_05_09.json"

required_doc_tokens = [
    "ZeroArityRepresentation",
    "ZeroArityRegistryReduction",
    "ZeroPositiveCarrierCaseSplit",
    "ZeroPositiveRegSNFReduction",
    "RepresentedZeroArityRegSNFFrontier",
    "RepresentedZeroArityRegSNFClosure",
    "UnrestrictedRegSNFDepthBridgeInterface",
    "UniversalFiberEntropyGapSeparationLock",
    "SemanticTwoPointUniversalFiberGapWitness",
    "AnalyticShannonEntropyBridgeFrontierLock",
    "SelectedDepthBridgeSemanticGapNonPromotion",
    "UniversalFiberEntropyGapWitnessInterface",
    "ChronosRRPromotionFrontierLock",
    "RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily",
    "selected-carrier DepthBridge interface",
    "AnalyticShannonEntropyBridge",
    "UniversalFiberEntropyGap from Reg-SNF",
    "DepthBridge extension beyond selected final carrier domain",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "Clay-problem closure",
    "does not prove UniversalFiberEntropyGap from Reg-SNF",
    "does not extend the DepthBridge interface beyond the selected final carrier domain",
]

for path in (DOC, ART):
    assert path.exists(), f"missing {path}"

text = DOC.read_text()
for token in required_doc_tokens:
    assert token in text, token

data = json.loads(ART.read_text())
assert data["artifact"] == "open_frontier_status_snapshot_2026_05_09"
assert data["date"] == "2026-05-09"
assert data["status"] == "FRONTIER_OPEN"

closed = set(data["closed_verified_surfaces"])
for token in required_doc_tokens[:13]:
    assert token in closed, token

open_frontiers = set(data["open_frontiers"])
for token in [
    "AnalyticShannonEntropyBridge",
    "UniversalFiberEntropyGap from Reg-SNF",
    "DepthBridge extension beyond selected final carrier domain",
    "Chronos-RR promotion",
    "H4.1/FGL",
    "P vs NP",
    "Clay-problem closure",
]:
    assert token in open_frontiers, token

boundary = " ".join(data["boundary"])
for token in [
    "does not prove UniversalFiberEntropyGap from Reg-SNF",
    "does not extend DepthBridge beyond selected final carrier domain",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove P vs NP",
    "does not prove Clay-problem closure",
]:
    assert token in boundary, token

print("open frontier status snapshot verified: FRONTIER_OPEN")
