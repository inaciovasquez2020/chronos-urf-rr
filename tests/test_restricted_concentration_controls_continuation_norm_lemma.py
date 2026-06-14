from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/RestrictedConcentrationControlsContinuationNormLemma.lean"


def test_restricted_concentration_controls_continuation_norm_lemma_surface_tokens():
    text = LEAN.read_text()
    assert "structure RestrictedConcentrationControlsContinuationNormLemmaData" in text
    assert "structure RestrictedConcentrationControlsContinuationNormLemmaHypotheses" in text
    assert "theorem RestrictedConcentrationControlsContinuationNormLemmaSurface" in text
    assert "RESTRICTED_CONCENTRATION_CONTROLS_CONTINUATION_NORM_LEMMA" in text


def test_restricted_concentration_controls_continuation_norm_lemma_boundary():
    text = LEAN.read_text()
    assert "LEMMA_SURFACE_ONLY_NO_ANALYTIC_CONTINUATION_NORM_CONTROL_PROOF" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF" in text
    assert "NO_UNCONDITIONAL_RESTRICTED_CONTINUATION_NORM_CONTROL_THEOREM" in text
    assert "does not prove unconditional restricted continuation norm control" in text


def test_restricted_concentration_controls_continuation_norm_lemma_no_proof_holes():
    text = LEAN.read_text()
    assert "axiom " not in text
    assert "opaque " not in text
    assert "sorry" not in text
    assert "admit" not in text
