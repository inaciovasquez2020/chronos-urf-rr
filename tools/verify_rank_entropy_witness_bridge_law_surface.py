#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/RankEntropyWitnessBridgeLawSurface.lean"
DOC = ROOT / "docs/status/CHRONOS_RANK_ENTROPY_WITNESS_BRIDGE_LAW_SURFACE_2026_05_13.md"
ARTIFACT = ROOT / "artifacts/chronos/rank_entropy_witness_bridge_law_surface_2026_05_13.json"
ROOT_IMPORT = ROOT / "Chronos.lean"

lean = LEAN.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())
root_import = ROOT_IMPORT.read_text()

required_lean_tokens = [
    "theorem rankEntropyWitnessBridgeLaw_surface",
    "theorem semanticRankRateToFiberEntropySoundness_repository_native_surface",
    "RankEntropyWitnessBridgeLaw",
    "SemanticRankRateToFiberEntropySoundness",
    "BRIDGE_SURFACE_CLOSED_ONLY",
]

for token in required_lean_tokens:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit", "axiom"]:
    if forbidden in lean:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.RankEntropyWitnessBridgeLawSurface" not in root_import:
    raise SystemExit("missing Chronos.lean import")

if artifact["status"] != "BRIDGE_SURFACE_CLOSED_ONLY":
    raise SystemExit("artifact status mismatch")

if artifact["frontier_open_preserved_for_unrestricted_chronos"] is not True:
    raise SystemExit("unrestricted frontier preservation mismatch")

if artifact["theorem_level_closure"] is not False:
    raise SystemExit("theorem_level_closure must be false")

required_doc_tokens = [
    "Status: BRIDGE_SURFACE_CLOSED_ONLY",
    "rankEntropyWitnessBridgeLaw_surface",
    "semanticRankRateToFiberEntropySoundness_repository_native_surface",
    "RankEntropyWitnessBridgeLaw is closed only on the current repository-native formal surface.",
    "SemanticRankRateToFiberEntropySoundness is closed only on the current repository-native formal surface.",
    "This does not prove unrestricted UniversalFiberEntropyGap.",
    "This does not prove Chronos-RR.",
    "This does not close H4.1/FGL.",
    "This does not prove P vs NP.",
    "This does not solve any Clay problem.",
]

for token in required_doc_tokens:
    if token not in doc:
        raise SystemExit(f"missing doc token: {token}")

forbidden_claims = [
    "unrestricted UniversalFiberEntropyGap is proved",
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

print("RankEntropyWitnessBridgeLaw surface verified.")
