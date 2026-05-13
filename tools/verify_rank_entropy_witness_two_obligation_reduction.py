#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/RankEntropyWitnessTwoObligationReduction.lean"
DOC = ROOT / "docs/status/CHRONOS_RANK_ENTROPY_WITNESS_TWO_OBLIGATION_REDUCTION_2026_05_13.md"
ARTIFACT = ROOT / "artifacts/chronos/rank_entropy_witness_two_obligation_reduction_2026_05_13.json"
ROOT_IMPORT = ROOT / "Chronos.lean"

lean = LEAN.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())
root_import = ROOT_IMPORT.read_text()

required_lean_tokens = [
    "def LiveRankEntropyWitnessSelector",
    "def RankEntropyWitnessBridgeLaw",
    "theorem nonPropRankEntropyWitnessFrontier_from_selector_and_bridge",
    "theorem semanticRankRateToFiberEntropySoundness_from_selector_and_bridge",
    "NonPropRankEntropyWitnessFrontier",
    "SemanticRankRateToFiberEntropySoundness",
    "FRONTIER_OPEN / TWO_OBLIGATION_REDUCTION_ONLY",
]

for token in required_lean_tokens:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit", "axiom"]:
    if forbidden in lean:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.RankEntropyWitnessTwoObligationReduction" not in root_import:
    raise SystemExit("missing Chronos.lean import")

if artifact["status"] != "FRONTIER_OPEN / TWO_OBLIGATION_REDUCTION_ONLY":
    raise SystemExit("artifact status mismatch")

if artifact["frontier_open_preserved"] is not True:
    raise SystemExit("frontier_open_preserved must be true")

if artifact["theorem_level_closure"] is not False:
    raise SystemExit("theorem_level_closure must be false")

if artifact["remaining_obligations"] != [
    "LiveRankEntropyWitnessSelector",
    "RankEntropyWitnessBridgeLaw",
]:
    raise SystemExit("remaining obligations mismatch")

required_doc_tokens = [
    "Status: FRONTIER_OPEN / TWO_OBLIGATION_REDUCTION_ONLY",
    "LiveRankEntropyWitnessSelector",
    "RankEntropyWitnessBridgeLaw",
    "FRONTIER_OPEN is preserved.",
    "This is a two-obligation reduction only.",
    "No LiveRankEntropyWitnessSelector theorem is claimed.",
    "No RankEntropyWitnessBridgeLaw theorem is claimed.",
    "No unrestricted UniversalFiberEntropyGap theorem is claimed.",
    "No Chronos-RR theorem closure is claimed.",
    "No H4.1/FGL closure is claimed.",
    "No P vs NP closure is claimed.",
    "No Clay-problem closure is claimed.",
]

for token in required_doc_tokens:
    if token not in doc:
        raise SystemExit(f"missing doc token: {token}")

forbidden_claims = [
    "LiveRankEntropyWitnessSelector is proved",
    "RankEntropyWitnessBridgeLaw is proved",
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR is proved",
    "H4.1/FGL is closed",
    "P vs NP is proved",
    "Clay problem is solved",
    "unconditional theorem-level closure",
]

combined = "\n".join([lean, doc, json.dumps(artifact)])
for token in forbidden_claims:
    if token in combined:
        raise SystemExit(f"forbidden overclaim present: {token}")

print("RankEntropyWitness two-obligation reduction verified.")
