from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/status/CHRONOS_PREFIX_CONDITIONING_EMBEDDING_2026_05_03.md"
ART = ROOT / "artifacts/chronos/prefix_conditioning_embedding_2026_05_03.json"
VERIFY = ROOT / "scripts/verify_chronos_prefix_conditioning_embedding.py"

def test_prefix_conditioning_doc_exists_and_has_status():
    text = DOC.read_text()
    assert "Status: CONDITIONAL_PREFIX_EMBEDDING_REDUCTION" in text
    assert "The false leave-one-out target" in text
    assert "is replaced by prefix conditioning" in text

def test_prefix_coordinate_contributions_are_defined():
    text = DOC.read_text()
    assert "\\alpha_i^\\sigma" in text
    assert "I(X_{\\sigma(i)};T\\mid Y,X_{\\sigma(<i)})" in text
    assert "\\beta_i^\\sigma" in text
    assert "I(Y_{\\sigma(i)};T\\mid X,Y_{\\sigma(<i)})" in text

def test_chain_rule_identity_is_recorded():
    text = DOC.read_text()
    assert "IC_{\\mu_n}(\\Pi)" in text
    assert "\\sum_{i=1}^n" in text
    assert "\\mathbb E_\\sigma[" in text
    assert "\\mathbb E_{\\sigma,I}" in text
    assert "\\frac1n IC_{\\mu_n}(\\Pi)" in text

def test_prefix_embedding_bound_is_conditional():
    text = DOC.read_text()
    assert "\\mathrm{PrefixEmb}_n" in text
    assert "conditionally on the exact prefix pushforward construction" in text
    assert "\\mathrm{PrefixEmb}_{n\\#}\\zeta=\\mu_n" in text

def test_no_forbidden_overclaim_language():
    text = DOC.read_text()
    forbidden = [
        "P≠NP is proved",
        "P != NP is proved",
        "unconditional theorem-level closure is proved",
        "terminal Chronos lower bound is proved",
        "frontier closed unconditionally",
        "solves P vs NP",
    ]
    for token in forbidden:
        assert token not in text

def test_artifact_boundary_fields():
    data = json.loads(ART.read_text())
    assert data["status"] == "CONDITIONAL_PREFIX_EMBEDDING_REDUCTION"
    assert data["replacement"] == "prefix_conditioning_chain_rule_bound"
    assert data["boundary"]["unconditional_theorem_closure"] is False
    assert data["boundary"]["p_not_np_claim"] is False
    assert data["boundary"]["terminal_chronos_lower_bound_claimed"] is False
    assert data["boundary"]["frontier_preserved"] is True

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "CONDITIONAL_PREFIX_EMBEDDING_REDUCTION" in result.stdout
