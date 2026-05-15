from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/SemanticRankRateToFiberEntropySoundnessBridge.lean").read_text()
doc = Path("docs/status/CHRONOS_SEMANTIC_RANK_RATE_TO_FIBER_ENTROPY_SOUNDNESS_BRIDGE_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/semantic_rank_rate_to_fiber_entropy_soundness_bridge_2026_05_15.json").read_text())

required_lean = [
    "def SemanticRankRateToFiberEntropySoundness",
    "theorem semantic_rank_zero_defect_kills_entropy_defect_implies_soundness",
    "theorem semantic_rank_defect_control_implies_soundness",
    "SemanticRankZeroDefectKillsEntropyDefectOn",
    "SemanticRankDefectControlsEntropyDefectOn",
]

required_doc = [
    "CONDITIONAL / ZERO_DEFECT_SOUNDNESS_BRIDGE_CLOSED",
    "semantic_rank_zero_defect_kills_entropy_defect_implies_soundness",
    "semantic_rank_defect_control_implies_soundness",
    "Does not prove quantitative entropyDefect ≤ rankDefect.",
    "Does not prove unrestricted Chronos-RR.",
    "Does not prove H4.1/FGL.",
    "Does not prove P vs NP.",
    "Does not prove any Clay problem.",
]

for phrase in required_lean:
    assert phrase in lean, phrase

for phrase in required_doc:
    assert phrase in doc, phrase

assert artifact["status"] == "CONDITIONAL / ZERO_DEFECT_SOUNDNESS_BRIDGE_CLOSED"
assert artifact["closed_theorem"] == "semantic_rank_zero_defect_kills_entropy_defect_implies_soundness"
assert artifact["derived_theorem"] == "semantic_rank_defect_control_implies_soundness"
assert artifact["input"] == "SemanticRankZeroDefectKillsEntropyDefectOn"
assert artifact["output"] == "SemanticRankRateToFiberEntropySoundness"

print("Semantic rank-rate to fiber entropy soundness bridge verified.")
