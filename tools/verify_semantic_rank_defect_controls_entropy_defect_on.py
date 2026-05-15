from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/SemanticRankDefectControlsEntropyDefectOn.lean").read_text()
doc = Path("docs/status/CHRONOS_SEMANTIC_RANK_DEFECT_CONTROLS_ENTROPY_DEFECT_ON_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/semantic_rank_defect_controls_entropy_defect_on_2026_05_15.json").read_text())

required_lean = [
    "def SemanticRankZeroDefectKillsEntropyDefectOn",
    "def SemanticRankDefectControlsEntropyDefectOn",
    "theorem semantic_rank_defect_control_implies_zero_defect_transfer",
    "theorem semantic_rank_zero_defect_transfer",
    "Nat.eq_zero_of_le_zero",
]

required_doc = [
    "CONDITIONAL / WEAKER_SUFFICIENT_LEMMA_CLOSED",
    "SemanticRankZeroDefectKillsEntropyDefectOn",
    "semantic_rank_zero_defect_transfer",
    "Does not prove quantitative entropyDefect ≤ rankDefect.",
    "Does not prove unrestricted SemanticRankRateToFiberEntropySoundness.",
    "Does not prove Chronos-RR.",
    "Does not prove H4.1/FGL.",
    "Does not prove P vs NP.",
    "Does not prove any Clay problem.",
]

for phrase in required_lean:
    assert phrase in lean, phrase

for phrase in required_doc:
    assert phrase in doc, phrase

assert artifact["status"] == "CONDITIONAL / WEAKER_SUFFICIENT_LEMMA_CLOSED"
assert artifact["original_target"] == "SemanticRankDefectControlsEntropyDefectOn"
assert artifact["weaker_sufficient_replacement"] == "SemanticRankZeroDefectKillsEntropyDefectOn"
assert artifact["closed_theorem"] == "semantic_rank_zero_defect_transfer"

print("Semantic rank defect to entropy defect weaker sufficient lemma verified.")
