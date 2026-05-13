import json
from pathlib import Path

LEAN = Path("Chronos/Frontier/NonPropSemanticRankRateToFiberEntropySoundness.lean")
ARTIFACT = Path("artifacts/chronos/nonprop_semantic_rank_rate_to_fiber_entropy_soundness_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_NONPROP_SEMANTIC_RANK_RATE_TO_FIBER_ENTROPY_SOUNDNESS_2026_05_13.md")

def test_nonprop_numerical_fields_exist():
    text = LEAN.read_text()
    assert "rankRateGap : ℚ" in text
    assert "fiberEntropyGap : ℚ" in text
    assert "fiberEntropyGap_le_rankRateGap" in text

def test_main_theorem_and_canonical_witness_exist():
    text = LEAN.read_text()
    assert "theorem nonprop_semantic_rank_rate_to_fiber_entropy_soundness" in text
    assert "theorem canonical_nonprop_semantic_rank_rate_to_fiber_entropy_soundness" in text

def test_no_axiom_admit_or_sorry():
    text = LEAN.read_text()
    assert "axiom" not in text
    assert "admit" not in text
    assert "sorry" not in text

def test_artifact_boundary():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "NONPROP_NUMERICAL_SOUNDNESS_SURFACE_SOLVED"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False
    boundary = "\n".join(data["boundary"])
    assert "Does not prove UniversalFiberEntropyGap." in boundary
    assert "Does not prove Chronos-RR closure." in boundary
    assert "Does not prove P vs NP closure." in boundary

def test_status_doc_boundary():
    text = DOC.read_text()
    assert "Status: NONPROP_NUMERICAL_SOUNDNESS_SURFACE_SOLVED" in text
    assert "Does not prove unrestricted SemanticRankRateToFiberEntropySoundness." in text
    assert "Does not prove any Clay-problem closure." in text
