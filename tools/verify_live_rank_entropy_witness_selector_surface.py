#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/LiveRankEntropyWitnessSelectorSurface.lean"
DOC = ROOT / "docs/status/CHRONOS_LIVE_RANK_ENTROPY_WITNESS_SELECTOR_SURFACE_2026_05_13.md"
ARTIFACT = ROOT / "artifacts/chronos/live_rank_entropy_witness_selector_surface_2026_05_13.json"
ROOT_IMPORT = ROOT / "Chronos.lean"

lean = LEAN.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())
root_import = ROOT_IMPORT.read_text()

required_lean_tokens = [
    "def canonicalRankEntropyWitness",
    "def canonicalRankEntropyWitnessSet",
    "theorem canonicalRankEntropyWitnessSet_nonempty",
    "theorem canonicalRankEntropyWitness_live",
    "theorem canonicalRankEntropyWitnessSet_is_nonPropWitnessSet",
    "theorem liveRankEntropyWitnessSelector_surface",
    "SELECTOR_SURFACE_CLOSED_ONLY",
    "RankEntropyWitnessBridgeLaw",
]

for token in required_lean_tokens:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit", "axiom"]:
    if forbidden in lean:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.LiveRankEntropyWitnessSelectorSurface" not in root_import:
    raise SystemExit("missing Chronos.lean import")

if artifact["status"] != "SELECTOR_SURFACE_CLOSED_ONLY":
    raise SystemExit("artifact status mismatch")

if artifact["closed_obligation"] != "LiveRankEntropyWitnessSelector":
    raise SystemExit("closed obligation mismatch")

if artifact["remaining_obligation"] != "RankEntropyWitnessBridgeLaw":
    raise SystemExit("remaining obligation mismatch")

if artifact["theorem_level_closure"] is not False:
    raise SystemExit("theorem_level_closure must be false")

required_doc_tokens = [
    "Status: SELECTOR_SURFACE_CLOSED_ONLY",
    "liveRankEntropyWitnessSelector_surface",
    "RankEntropyWitnessBridgeLaw remains open.",
    "SemanticRankRateToFiberEntropySoundness is not closed unconditionally.",
    "FRONTIER_OPEN is preserved for the full bridge.",
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
    "RankEntropyWitnessBridgeLaw is proved",
    "SemanticRankRateToFiberEntropySoundness is closed unconditionally",
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR is proved",
    "H4.1/FGL is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]

combined = "\n".join([lean, doc, json.dumps(artifact)])
for token in forbidden_claims:
    if token in combined:
        raise SystemExit(f"forbidden overclaim present: {token}")

print("LiveRankEntropyWitnessSelector surface verified.")
