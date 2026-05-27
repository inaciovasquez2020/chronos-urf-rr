#!/usr/bin/env python3
import json
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/ConcreteNonToyApplicationRankGapExtraction.lean")
ART = Path("artifacts/chronos/concrete_non_toy_application_rank_gap_extraction_2026_05_27.json")
DOC = Path("docs/status/CONCRETE_NON_TOY_APPLICATION_RANK_GAP_EXTRACTION_2026_05_27.md")
ROOT = Path("lean/Chronos.lean")

for path in [LEAN, ART, DOC, ROOT]:
    assert path.exists(), f"missing required file: {path}"

src = LEAN.read_text()
artifact_text = ART.read_text()
doc_text = DOC.read_text()
root_text = ROOT.read_text()
data = json.loads(artifact_text)

required_src_tokens = [
    "ConcreteNonToyApplicationDataPacket",
    "concreteFiniteRegisteredHyperbolicPacket",
    "extractedConcreteSemanticRankRate",
    "extractedConcreteFiberEntropyGap",
    "extractedConcreteRankGapSlack",
    "concreteNonToyApplicationRankGapInequality",
    "concreteNonToyApplication_extracted_rank_eq",
    "concreteNonToyApplication_extracted_gap_eq",
    "concreteNonToyApplication_extracted_slack_eq",
    "concreteNonToyApplication_extracted_rank_plus_slack_le_gap",
    "concreteNonToyApplication_extracted_rank_lt_gap",
]

required_artifact_tokens = [
    "CONCRETE_NON_TOY_APPLICATION_RANK_GAP_EXTRACTION_CLOSED_DATA_PACKET_ONLY",
    "concreteNonToyApplicationRankGapExtraction",
    "replace finite list-length extraction packet with proof extracted from real target semantics and registry construction",
]

required_doc_tokens = [
    "CONCRETE_NON_TOY_APPLICATION_RANK_GAP_EXTRACTION_CLOSED_DATA_PACKET_ONLY",
    "ConcreteNonToyApplicationDataPacket",
    "Does not prove",
    "real target semantic extraction",
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

assert "import Chronos.Frontier.ConcreteNonToyApplicationRankGapExtraction" in root_text

assert data["status"] == "CONCRETE_NON_TOY_APPLICATION_RANK_GAP_EXTRACTION_CLOSED_DATA_PACKET_ONLY"
assert data["object"] == "concreteNonToyApplicationRankGapExtraction"
assert data["semantic_rank_rate_extracted"] + data["slack_extracted"] <= data["fiber_entropy_gap_extracted"]
assert data["slack_extracted"] > 0

for forbidden in [
    "proves UniversalFiberEntropyGap",
    "proves Chronos-RR",
    "proves P vs NP",
    "proves any Clay problem",
]:
    assert forbidden not in src
    assert forbidden not in artifact_text
    assert forbidden not in doc_text

print("CONCRETE_NON_TOY_APPLICATION_RANK_GAP_EXTRACTION_OK")
print(json.dumps({
    "object": data["object"],
    "status": data["status"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
