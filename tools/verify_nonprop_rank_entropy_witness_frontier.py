#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/NonPropRankEntropyWitnessFrontier.lean"
DOC = ROOT / "docs/status/CHRONOS_NONPROP_RANK_ENTROPY_WITNESS_FRONTIER_2026_05_13.md"
ARTIFACT = ROOT / "artifacts/chronos/nonprop_rank_entropy_witness_frontier_2026_05_13.json"
ROOT_IMPORT = ROOT / "Chronos.lean"

lean = LEAN.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())
root_import = ROOT_IMPORT.read_text()

required_lean_tokens = [
    "structure RankEntropyWitness",
    "fiber : FiberWitness",
    "rankMass : Nat",
    "entropyMass : Nat",
    "def RankEntropyWitnessLive",
    "def NonPropWitnessSet",
    "def NonPropRankEntropyWitnessFrontier",
    "def BridgeSoundnessFromNonPropRankEntropyWitness",
    "theorem bridge_soundness_from_nonPropRankEntropyWitness",
    "FRONTIER_OPEN / WEAKEST_MISSING_NONPROP_WITNESS_ONLY",
]

for token in required_lean_tokens:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit", "axiom"]:
    if forbidden in lean:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.NonPropRankEntropyWitnessFrontier" not in root_import:
    raise SystemExit("missing Chronos.lean import")

if artifact["status"] != "FRONTIER_OPEN / WEAKEST_MISSING_NONPROP_WITNESS_ONLY":
    raise SystemExit("artifact status mismatch")

if artifact["frontier_open_preserved"] is not True:
    raise SystemExit("frontier_open_preserved must be true")

if artifact["theorem_level_closure"] is not False:
    raise SystemExit("theorem_level_closure must be false")

if artifact["bridge"]["conditional"] is not True:
    raise SystemExit("bridge must remain conditional")

if artifact["weakest_missing_object"] != "NonPropRankEntropyWitnessFrontier":
    raise SystemExit("weakest missing object mismatch")

required_doc_tokens = [
    "Status: FRONTIER_OPEN / WEAKEST_MISSING_NONPROP_WITNESS_ONLY",
    "structure RankEntropyWitness",
    "rankMass : Nat",
    "entropyMass : Nat",
    "FRONTIER_OPEN is preserved.",
    "This records the weakest missing non-Prop witness object only.",
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

print("NonPropRankEntropyWitness frontier verified.")
