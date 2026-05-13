import json
from pathlib import Path

LEAN = Path("Chronos/Frontier/UniversalFiberEntropyGapFromNonPropSoundness.lean")
ARTIFACT = Path("artifacts/chronos/universal_fiber_entropy_gap_from_nonprop_soundness_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_UNIVERSAL_FIBER_ENTROPY_GAP_FROM_NONPROP_SOUNDNESS_2026_05_13.md")

def test_gap_surface_exists():
    text = LEAN.read_text()
    assert "def RepositoryNativeUniversalFiberEntropyGap : Prop" in text
    assert "∃ ε : ℚ, 0 < ε" in text

def test_bridge_uses_nonprop_soundness():
    text = LEAN.read_text()
    assert "repository_native_universal_fiber_entropy_gap_from_nonprop_soundness" in text
    assert "nonprop_semantic_rank_rate_to_fiber_entropy_soundness D" in text

def test_canonical_witness_exists():
    text = LEAN.read_text()
    assert "canonical_repository_native_universal_fiber_entropy_gap" in text
    assert "canonicalNonPropSemanticRankRateDatum" in text

def test_no_axiom_admit_or_sorry():
    text = LEAN.read_text()
    assert "axiom" not in text
    assert "admit" not in text
    assert "sorry" not in text

def test_artifact_boundary():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "REPOSITORY_NATIVE_NUMERICAL_GAP_WITNESS_SOLVED"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False
    boundary = "\n".join(data["boundary"])
    assert "Does not prove unrestricted UniversalFiberEntropyGap." in boundary
    assert "Does not prove Chronos-RR closure." in boundary
    assert "Does not prove P vs NP closure." in boundary

def test_status_doc_boundary():
    text = DOC.read_text()
    assert "Status: REPOSITORY_NATIVE_NUMERICAL_GAP_WITNESS_SOLVED" in text
    assert "Does not prove unrestricted UniversalFiberEntropyGap." in text
    assert "Does not prove any Clay-problem closure." in text
