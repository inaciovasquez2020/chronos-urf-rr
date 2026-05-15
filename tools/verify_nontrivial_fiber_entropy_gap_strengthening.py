from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/NontrivialFiberEntropyGapStrengthening.lean").read_text()
doc = Path("docs/status/CHRONOS_NONTRIVIAL_FIBER_ENTROPY_GAP_STRENGTHENING_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/nontrivial_fiber_entropy_gap_strengthening_2026_05_15.json").read_text())

required_lean = [
    "def CanonicalToNontrivialFiberEntropyGapStrengthening",
    "theorem canonical_strengthening_implies_nontrivial_fiber_gap",
    "theorem semantic_rank_rate_soundness_implies_nontrivial_fiber_gap",
    "theorem semantic_rank_defect_control_implies_nontrivial_fiber_gap",
    "CanonicalZeroEntropyFiberGap",
    "SemanticRankRateToFiberEntropySoundness",
    "SemanticRankDefectControlsEntropyDefectOn",
]

required_doc = [
    "CONDITIONAL / STRENGTHENING_INTERFACE_ISOLATED",
    "CanonicalToNontrivialFiberEntropyGapStrengthening",
    "canonical_strengthening_implies_nontrivial_fiber_gap",
    "semantic_rank_rate_soundness_implies_nontrivial_fiber_gap",
    "semantic_rank_defect_control_implies_nontrivial_fiber_gap",
    "Does not construct a nontrivial UniversalFiberEntropyGap.",
    "Does not prove the strengthening interface.",
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

assert artifact["status"] == "CONDITIONAL / STRENGTHENING_INTERFACE_ISOLATED"
assert artifact["strengthening_interface"] == "CanonicalToNontrivialFiberEntropyGapStrengthening"
assert artifact["closed_theorem"] == "canonical_strengthening_implies_nontrivial_fiber_gap"
assert artifact["downstream_theorem"] == "semantic_rank_rate_soundness_implies_nontrivial_fiber_gap"
assert artifact["derived_theorem"] == "semantic_rank_defect_control_implies_nontrivial_fiber_gap"
assert artifact["weakest_remaining_object"] == "CanonicalToNontrivialFiberEntropyGapStrengthening"

print("Nontrivial fiber entropy gap strengthening interface verified.")
