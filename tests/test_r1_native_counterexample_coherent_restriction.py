import json
import re
from pathlib import Path


def test_r1_native_counterexample_artifact_status_and_claims():
    data = json.loads(
        Path("artifacts/chronos/r1_native_counterexample_coherent_restriction_2026_05_24.json").read_text()
    )
    assert data["status"] == "UNRESTRICTED_R1_FALSE_COHERENT_R1_CLOSED"
    assert data["claims"]["unrestricted_native_r1_long_chord_exclusion_false"] is True
    assert data["claims"]["coherent_native_r1_long_chord_exclusion_closed"] is True
    assert data["claims"]["opaque_LongChordExclusionProofTarget_closed"] is False
    assert data["claims"]["theorem_level_R1_promotion_closed"] is False
    assert data["claims"]["R2_closed"] is False
    assert data["claims"]["R3_closed"] is False
    assert data["claims"]["NON_FACTORISATION_closed"] is False
    assert data["claims"]["Chronos_RR_closed"] is False
    assert data["claims"]["H4_1_FGL_closed"] is False
    assert data["claims"]["P_vs_NP_closed"] is False
    assert data["claims"]["Clay_problem_closed"] is False


def test_r1_native_counterexample_doc_boundaries():
    text = Path("docs/status/R1_NATIVE_COUNTEREXAMPLE_COHERENT_RESTRICTION_2026_05_24.md").read_text()
    for token in [
        "does not prove opaque LongChordExclusionProofTarget",
        "does not prove theorem-level R1 promotion",
        "does not prove R2",
        "does not prove R3",
        "does not prove NON_FACTORISATION",
        "does not prove Chronos-RR",
        "does not prove H4.1/FGL",
        "does not prove P vs NP",
        "does not prove any Clay problem",
    ]:
        assert token in text


def test_r1_native_counterexample_lean_surface():
    text = Path("lean/Chronos/Frontier/R1NativeCounterexampleCoherentRestriction.lean").read_text()
    assert not re.search(r"(?m)^\\s*axiom\\b", text)
    assert not re.search(r"(?m)^\\s*opaque\\b", text)
    for token in [
        "R1NativeLongChordCounterexampleObject",
        "R1NativeLongChordCounterexampleObject_is_witness",
        "R1UnrestrictedNativeLongChordExclusionFalse",
        "R1CoherentLongChordExclusionProofTarget",
        "R1CoherentLongChordExclusionProofTarget_proved",
        "R1WeakestSufficientNativeIngredientForLongChordExclusion",
        "R1WeakestSufficientNativeIngredientForLongChordExclusion_suffices",
        "UNRESTRICTED_R1_FALSE_COHERENT_R1_CLOSED",
    ]:
        assert token in text
