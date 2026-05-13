import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_live_rank_entropy_witness_selector_surface_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_live_rank_entropy_witness_selector_surface.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "LiveRankEntropyWitnessSelector surface verified." in result.stdout


def test_live_rank_entropy_witness_selector_surface_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/live_rank_entropy_witness_selector_surface_2026_05_13.json").read_text()
    )
    assert data["status"] == "SELECTOR_SURFACE_CLOSED_ONLY"
    assert data["closed_obligation"] == "LiveRankEntropyWitnessSelector"
    assert data["remaining_obligation"] == "RankEntropyWitnessBridgeLaw"
    assert data["theorem_level_closure"] is False


def test_live_rank_entropy_witness_selector_surface_lean_tokens():
    lean = (ROOT / "Chronos/Frontier/LiveRankEntropyWitnessSelectorSurface.lean").read_text()
    assert "def canonicalRankEntropyWitness" in lean
    assert "def canonicalRankEntropyWitnessSet" in lean
    assert "theorem canonicalRankEntropyWitnessSet_is_nonPropWitnessSet" in lean
    assert "theorem liveRankEntropyWitnessSelector_surface" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
    assert "axiom" not in lean


def test_live_rank_entropy_witness_selector_surface_boundary_doc():
    doc = (ROOT / "docs/status/CHRONOS_LIVE_RANK_ENTROPY_WITNESS_SELECTOR_SURFACE_2026_05_13.md").read_text()
    assert "RankEntropyWitnessBridgeLaw remains open." in doc
    assert "SemanticRankRateToFiberEntropySoundness is not closed unconditionally." in doc
    assert "FRONTIER_OPEN is preserved for the full bridge." in doc
    assert "No unrestricted UniversalFiberEntropyGap theorem is claimed." in doc
    assert "No Chronos-RR theorem closure is claimed." in doc
    assert "No H4.1/FGL closure is claimed." in doc
    assert "No P vs NP closure is claimed." in doc
    assert "No Clay-problem closure is claimed." in doc
