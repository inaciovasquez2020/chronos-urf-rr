#!/usr/bin/env python3
import json
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/SemanticRegistryRankGapExtraction.lean")
ART = Path("artifacts/chronos/semantic_registry_rank_gap_extraction_2026_05_27.json")
DOC = Path("docs/status/SEMANTIC_REGISTRY_RANK_GAP_EXTRACTION_2026_05_27.md")
ROOT = Path("lean/Chronos.lean")

for path in [LEAN, ART, DOC, ROOT]:
    assert path.exists(), f"missing required file: {path}"

src = LEAN.read_text()
artifact_text = ART.read_text()
doc_text = DOC.read_text()
root_text = ROOT.read_text()
data = json.loads(artifact_text)

required_src_tokens = [
    "SemanticRegistryRankGapConstruction",
    "finiteRegisteredHyperbolicSemanticRegistryConstruction",
    "semanticRegistryExtractedRankGapInequality",
    "semanticRegistry_rank_plus_slack_le_gap",
    "semanticRegistry_rank_lt_gap",
    "semanticRegistry_construction_exists",
    "semanticRankGapBound",
    "registryConstructed",
]

required_artifact_tokens = [
    "SEMANTIC_REGISTRY_RANK_GAP_EXTRACTION_CLOSED_CONSTRUCTION_FIELD_ONLY",
    "semanticRegistryRankGapExtraction",
    "replace semantic registry construction fields with repository-native semantic computation from the actual target registry",
]

required_doc_tokens = [
    "SEMANTIC_REGISTRY_RANK_GAP_EXTRACTION_CLOSED_CONSTRUCTION_FIELD_ONLY",
    "SemanticRegistryRankGapConstruction",
    "Does not prove",
    "repository-native semantic computation",
    "UniversalFiberEntropyGap",
    "Chronos-RR",
    "P vs NP",
    "any Clay problem",
]

for token in required_src_tokens:
    assert token in src, token

for token in required_artifact_tokens:
    assert token in artifact_text, token

for token in required_doc_tokens:
    assert token in doc_text, token

assert "import Chronos.Frontier.SemanticRegistryRankGapExtraction" in root_text

assert data["status"] == "SEMANTIC_REGISTRY_RANK_GAP_EXTRACTION_CLOSED_CONSTRUCTION_FIELD_ONLY"
assert data["object"] == "semanticRegistryRankGapExtraction"
assert data["semantic_rank_rate"] + data["semantic_slack"] <= data["fiber_entropy_gap"]
assert data["semantic_slack"] > 0

for forbidden in [
    "proves UniversalFiberEntropyGap",
    "proves Chronos-RR",
    "proves P vs NP",
    "proves any Clay problem",
]:
    assert forbidden not in src
    assert forbidden not in artifact_text
    assert forbidden not in doc_text

print("SEMANTIC_REGISTRY_RANK_GAP_EXTRACTION_OK")
print(json.dumps({
    "object": data["object"],
    "status": data["status"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
