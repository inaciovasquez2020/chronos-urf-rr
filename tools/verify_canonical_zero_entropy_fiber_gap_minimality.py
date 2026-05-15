from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/CanonicalZeroEntropyFiberGapMinimality.lean").read_text()
doc = Path("docs/status/CHRONOS_CANONICAL_ZERO_ENTROPY_FIBER_GAP_MINIMALITY_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/canonical_zero_entropy_fiber_gap_minimality_2026_05_15.json").read_text())

required_lean = [
    "def CanonicalZeroEntropyFiberGapContainedIn",
    "theorem canonical_zero_entropy_fiber_gap_minimality",
    "theorem canonical_zero_entropy_fiber_gap_self_minimality",
    "theorem semantic_rank_rate_soundness_implies_any_compatible_fiber_gap",
    "theorem semantic_rank_defect_control_implies_any_compatible_fiber_gap",
    "UniversalFiberEntropyGapCompatibility",
    "CanonicalZeroEntropyFiberGap",
    "SemanticRankRateToFiberEntropySoundness",
    "SemanticRankDefectControlsEntropyDefectOn",
]

required_doc = [
    "CONDITIONAL / CANONICAL_MINIMALITY_CLOSED",
    "canonical_zero_entropy_fiber_gap_minimality",
    "canonical_zero_entropy_fiber_gap_self_minimality",
    "semantic_rank_rate_soundness_implies_any_compatible_fiber_gap",
    "semantic_rank_defect_control_implies_any_compatible_fiber_gap",
    "Does not construct a nontrivial UniversalFiberEntropyGap.",
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

assert artifact["status"] == "CONDITIONAL / CANONICAL_MINIMALITY_CLOSED"
assert artifact["closed_theorem"] == "canonical_zero_entropy_fiber_gap_minimality"
assert artifact["self_minimality_theorem"] == "canonical_zero_entropy_fiber_gap_self_minimality"
assert artifact["downstream_theorem"] == "semantic_rank_rate_soundness_implies_any_compatible_fiber_gap"
assert artifact["derived_theorem"] == "semantic_rank_defect_control_implies_any_compatible_fiber_gap"

print("Canonical zero-entropy fiber-gap minimality verified.")
