from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/NontrivialFiberEntropyGapPredicate.lean").read_text()
doc = Path("docs/status/CHRONOS_NONTRIVIAL_FIBER_ENTROPY_GAP_PREDICATE_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/nontrivial_fiber_entropy_gap_predicate_2026_05_15.json").read_text())

required_lean = [
    "def NontrivialFiberEntropyGapPredicate",
    "def NontrivialFiberEntropyGapRefinesUniversal",
    "theorem canonical_zero_entropy_implies_nontrivial_fiber_entropy_gap_predicate",
    "theorem universal_compatibility_implies_nontrivial_refines_universal",
    "theorem semantic_rank_rate_soundness_implies_nontrivial_fiber_entropy_gap_predicate",
    "theorem semantic_rank_rate_soundness_implies_universal_from_nontrivial_relation",
    "CanonicalZeroEntropyFiberGap",
    "UniversalFiberEntropyGapCompatibility",
    "SemanticRankRateToFiberEntropySoundness",
]

required_doc = [
    "CONDITIONAL / PREDICATE_SURFACE_CLOSED",
    "NontrivialFiberEntropyGapPredicate",
    "NontrivialFiberEntropyGapRefinesUniversal",
    "canonical_zero_entropy_implies_nontrivial_fiber_entropy_gap_predicate",
    "universal_compatibility_implies_nontrivial_refines_universal",
    "semantic_rank_rate_soundness_implies_nontrivial_fiber_entropy_gap_predicate",
    "semantic_rank_rate_soundness_implies_universal_from_nontrivial_relation",
    "Does not construct a genuinely nontrivial UniversalFiberEntropyGap.",
    "Does not prove unrestricted UniversalFiberEntropyGap.",
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

for forbidden in [
    "Chronos-RR is proved",
    "H4.1/FGL is proved",
    "P vs NP is proved",
    "Clay problem is solved",
    "unrestricted Chronos-RR closure",
    "unrestricted theorem-level closure"
]:
    assert forbidden not in doc
    assert forbidden not in lean

assert artifact["status"] == "CONDITIONAL / PREDICATE_SURFACE_CLOSED"
assert artifact["predicate"] == "NontrivialFiberEntropyGapPredicate"
assert artifact["relation_to_universal"] == "NontrivialFiberEntropyGapRefinesUniversal"
assert artifact["closed_theorem"] == "canonical_zero_entropy_implies_nontrivial_fiber_entropy_gap_predicate"
assert artifact["dashboard_after_merge_only"] is True

print("Nontrivial fiber entropy gap predicate surface verified.")
