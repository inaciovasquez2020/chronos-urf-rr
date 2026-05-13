import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_rank_entropy_witness_bridge_law_surface_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_rank_entropy_witness_bridge_law_surface.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "RankEntropyWitnessBridgeLaw surface verified." in result.stdout


def test_rank_entropy_witness_bridge_law_surface_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/rank_entropy_witness_bridge_law_surface_2026_05_13.json").read_text()
    )
    assert data["status"] == "BRIDGE_SURFACE_CLOSED_ONLY"
    assert data["frontier_open_preserved_for_unrestricted_chronos"] is True
    assert data["theorem_level_closure"] is False
    assert "RankEntropyWitnessBridgeLaw" in data["closed_repository_native_surface"]
    assert "SemanticRankRateToFiberEntropySoundness" in data["closed_repository_native_surface"]


def test_rank_entropy_witness_bridge_law_surface_lean_tokens():
    lean = (ROOT / "Chronos/Frontier/RankEntropyWitnessBridgeLawSurface.lean").read_text()
    assert "theorem rankEntropyWitnessBridgeLaw_surface" in lean
    assert "theorem semanticRankRateToFiberEntropySoundness_repository_native_surface" in lean
    assert "BRIDGE_SURFACE_CLOSED_ONLY" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
    assert "axiom" not in lean


def test_rank_entropy_witness_bridge_law_surface_boundary_doc():
    doc = (ROOT / "docs/status/CHRONOS_RANK_ENTROPY_WITNESS_BRIDGE_LAW_SURFACE_2026_05_13.md").read_text()
    assert "RankEntropyWitnessBridgeLaw is closed only on the current repository-native formal surface." in doc
    assert "SemanticRankRateToFiberEntropySoundness is closed only on the current repository-native formal surface." in doc
    assert "This does not prove unrestricted UniversalFiberEntropyGap." in doc
    assert "This does not prove Chronos-RR." in doc
    assert "This does not close H4.1/FGL." in doc
    assert "This does not prove P vs NP." in doc
    assert "This does not solve any Clay problem." in doc
