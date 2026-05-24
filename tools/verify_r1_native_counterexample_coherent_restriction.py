from pathlib import Path
import json
import re

lean = Path("lean/Chronos/Frontier/R1NativeCounterexampleCoherentRestriction.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/r1_native_counterexample_coherent_restriction_2026_05_24.json").read_text())
doc = Path("docs/status/R1_NATIVE_COUNTEREXAMPLE_COHERENT_RESTRICTION_2026_05_24.md").read_text()
root = Path("lean/Chronos.lean").read_text()

assert not re.search(r"(?m)^\s*axiom\b", lean)
assert not re.search(r"(?m)^\s*opaque\b", lean)

required_lean = [
    "R1NativeLongChordCounterexampleObject",
    "R1NativeLongChordCounterexampleObject_is_witness",
    "R1UnrestrictedNativeLongChordExclusionFalse",
    "R1CoherentLongChordExclusionProofTarget",
    "R1CoherentLongChordExclusionProofTarget_proved",
    "R1WeakestSufficientNativeIngredientForLongChordExclusion",
    "R1WeakestSufficientNativeIngredientForLongChordExclusion_suffices",
    "UNRESTRICTED_R1_FALSE_COHERENT_R1_CLOSED",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "UNRESTRICTED_R1_FALSE_COHERENT_R1_CLOSED"
assert artifact["claims"]["unrestricted_native_r1_long_chord_exclusion_false"] is True
assert artifact["claims"]["coherent_native_r1_long_chord_exclusion_closed"] is True
assert artifact["claims"]["opaque_LongChordExclusionProofTarget_closed"] is False
assert artifact["claims"]["theorem_level_R1_promotion_closed"] is False
assert artifact["claims"]["R2_closed"] is False
assert artifact["claims"]["R3_closed"] is False
assert artifact["claims"]["NON_FACTORISATION_closed"] is False
assert artifact["claims"]["Chronos_RR_closed"] is False
assert artifact["claims"]["H4_1_FGL_closed"] is False
assert artifact["claims"]["P_vs_NP_closed"] is False
assert artifact["claims"]["Clay_problem_closed"] is False

for key in [
    "counterexample_object",
    "counterexample_theorem",
    "unrestricted_false_theorem",
    "restricted_target",
    "restricted_target_theorem",
    "weakest_sufficient_native_ingredient",
    "weakest_sufficient_theorem",
]:
    assert artifact[key] in lean or artifact[key] in doc, key

for boundary in artifact["boundary"]:
    assert boundary in doc, boundary

assert "import Chronos.Frontier.R1NativeCounterexampleCoherentRestriction" in root

print("R1 native counterexample coherent restriction verified.")
