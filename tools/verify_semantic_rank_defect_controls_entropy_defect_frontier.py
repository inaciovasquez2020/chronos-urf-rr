#!/usr/bin/env python3
from pathlib import Path
import json
import sys

lean = Path("Chronos/Frontier/SemanticRankDefectControlsEntropyDefectFrontier.lean")
doc = Path("docs/status/CHRONOS_SEMANTIC_RANK_DEFECT_CONTROLS_ENTROPY_DEFECT_FRONTIER_2026_05_12.md")
artifact = Path("artifacts/chronos/semantic_rank_defect_controls_entropy_defect_frontier_2026_05_12.json")
root = Path("Chronos.lean")

required_files = [lean, doc, artifact, root]
missing = [str(p) for p in required_files if not p.exists()]
if missing:
    print("Missing files:", missing)
    sys.exit(1)

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_text = artifact.read_text()
artifact_data = json.loads(artifact_text)
root_text = root.read_text()

required_lean_tokens = [
    "structure NonPropRankEntropyData",
    "fiberSize : ℕ",
    "imageSize : ℕ",
    "rankDefect : Rat",
    "entropyDefect : Rat",
    "def SemanticRankDefectControlsEntropyDefectOn",
    "def WeakestMissingTheoremLevelInput",
    "def DirectRankEntropyTransferOn",
    "def WeakestExecutableClosureInput",
    "theorem conditional_rank_rate_gap_to_fiber_entropy_gap_from_direct_transfer",
]

required_doc_tokens = [
    "FRONTIER_OPEN / WEAKEST_MISSING_QUANTITATIVE_LEMMA",
    "Weakest missing theorem-level input",
    "SemanticRankDefectControlsEntropyDefectOn",
    "does not prove RankRateGap",
    "UniversalFiberEntropyGap",
    "P vs NP",
    "Clay-problem closure",
]

required_artifact = {
    "status": "FRONTIER_OPEN / WEAKEST_MISSING_QUANTITATIVE_LEMMA",
    "weakest_missing_theorem_level_input": "SemanticRankDefectControlsEntropyDefectOn",
    "theorem_level_closure": False,
}

for token in required_lean_tokens:
    if token not in lean_text:
        print(f"Missing Lean token: {token}")
        sys.exit(1)

for token in required_doc_tokens:
    if token not in doc_text:
        print(f"Missing doc token: {token}")
        sys.exit(1)

for key, value in required_artifact.items():
    if artifact_data.get(key) != value:
        print(f"Artifact mismatch for {key}: expected {value!r}, got {artifact_data.get(key)!r}")
        sys.exit(1)

import_line = "import Chronos.Frontier.SemanticRankDefectControlsEntropyDefectFrontier"
if import_line not in root_text:
    print("Missing Chronos.lean import")
    sys.exit(1)

for forbidden in [
    "RankRateGap is proved",
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "P vs NP is proved",
    "Clay-problem closure is proved",
]:
    if forbidden in lean_text or forbidden in doc_text or forbidden in artifact_text:
        print(f"Forbidden overclaim token found: {forbidden}")
        sys.exit(1)

print("Semantic rank defect controls entropy defect frontier verified.")
