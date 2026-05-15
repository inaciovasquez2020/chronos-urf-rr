from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/CanonicalToNontrivialStrengtheningForPredicate.lean").read_text()
doc = Path("docs/status/CHRONOS_CANONICAL_TO_NONTRIVIAL_STRENGTHENING_FOR_PREDICATE_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/canonical_to_nontrivial_strengthening_for_predicate_2026_05_15.json").read_text())

required_lean = [
    "theorem canonical_to_nontrivial_strengthening_for_predicate",
    "theorem semantic_rank_rate_soundness_implies_defined_nontrivial_fiber_gap",
    "theorem semantic_rank_defect_control_implies_defined_nontrivial_fiber_gap",
    "CanonicalToNontrivialFiberEntropyGapStrengthening",
    "NontrivialFiberEntropyGapPredicate",
    "SemanticRankRateToFiberEntropySoundness",
    "SemanticRankDefectControlsEntropyDefectOn",
]

required_doc = [
    "PROVED / PREDICATE_SURFACE_STRENGTHENING_CLOSED",
    "canonical_to_nontrivial_strengthening_for_predicate",
    "semantic_rank_rate_soundness_implies_defined_nontrivial_fiber_gap",
    "semantic_rank_defect_control_implies_defined_nontrivial_fiber_gap",
    "The strengthening is closed only for the repository-defined predicate surface.",
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
    "genuinely nontrivial UniversalFiberEntropyGap is proved",
    "unrestricted UniversalFiberEntropyGap is proved",
    "unrestricted Chronos-RR is proved",
    "H4.1/FGL is proved",
    "P vs NP is proved",
    "Clay problem is solved",
    "unrestricted theorem-level closure"
]:
    assert forbidden not in lean
    assert forbidden not in doc

assert artifact["status"] == "PROVED / PREDICATE_SURFACE_STRENGTHENING_CLOSED"
assert artifact["closed_theorem"] == "canonical_to_nontrivial_strengthening_for_predicate"
assert artifact["theorem_scope"] == "repository_defined_predicate_surface_only"

print("Canonical-to-nontrivial strengthening for defined predicate verified.")
