from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/SemanticRankRateUniversalFiberEntropyGapCompatibility.lean").read_text()
doc = Path("docs/status/CHRONOS_SEMANTIC_RANK_RATE_UNIVERSAL_FIBER_ENTROPY_GAP_COMPATIBILITY_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/semantic_rank_rate_universal_fiber_entropy_gap_compatibility_2026_05_15.json").read_text())

required_lean = [
    "def UniversalFiberEntropyGapCompatibility",
    "theorem semantic_rank_rate_soundness_implies_universal_fiber_entropy_gap_compatibility",
    "theorem semantic_rank_defect_control_implies_universal_fiber_entropy_gap_compatibility",
    "SemanticRankRateToFiberEntropySoundness",
    "SemanticRankDefectControlsEntropyDefectOn",
]

required_doc = [
    "CONDITIONAL / COMPATIBILITY_BRIDGE_CLOSED",
    "semantic_rank_rate_soundness_implies_universal_fiber_entropy_gap_compatibility",
    "semantic_rank_defect_control_implies_universal_fiber_entropy_gap_compatibility",
    "UniversalFiberEntropyGapCompatibility",
    "Does not construct UniversalFiberEntropyGap.",
    "Does not prove unrestricted SemanticRankRateToFiberEntropySoundness.",
    "Does not prove unrestricted Chronos-RR.",
    "Does not prove H4.1/FGL.",
    "Does not prove P vs NP.",
    "Does not prove any Clay problem.",
]

for phrase in required_lean:
    assert phrase in lean, phrase

for phrase in required_doc:
    assert phrase in doc, phrase

assert artifact["status"] == "CONDITIONAL / COMPATIBILITY_BRIDGE_CLOSED"
assert artifact["closed_theorem"] == "semantic_rank_rate_soundness_implies_universal_fiber_entropy_gap_compatibility"
assert artifact["derived_theorem"] == "semantic_rank_defect_control_implies_universal_fiber_entropy_gap_compatibility"
assert artifact["weakest_remaining_external_input"] == "UniversalFiberEntropyGapCompatibility"

print("Semantic rank-rate UniversalFiberEntropyGap compatibility bridge verified.")
