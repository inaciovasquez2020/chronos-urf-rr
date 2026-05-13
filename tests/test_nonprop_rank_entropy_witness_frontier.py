import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_nonprop_rank_entropy_witness_frontier_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_nonprop_rank_entropy_witness_frontier.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "NonPropRankEntropyWitness frontier verified." in result.stdout


def test_nonprop_rank_entropy_witness_frontier_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/nonprop_rank_entropy_witness_frontier_2026_05_13.json").read_text()
    )
    assert data["status"] == "FRONTIER_OPEN / WEAKEST_MISSING_NONPROP_WITNESS_ONLY"
    assert data["frontier_open_preserved"] is True
    assert data["theorem_level_closure"] is False
    assert data["bridge"]["conditional"] is True
    assert data["weakest_missing_object"] == "NonPropRankEntropyWitnessFrontier"


def test_nonprop_rank_entropy_witness_frontier_lean_tokens():
    lean = (ROOT / "Chronos/Frontier/NonPropRankEntropyWitnessFrontier.lean").read_text()
    assert "structure RankEntropyWitness" in lean
    assert "rankMass : Nat" in lean
    assert "entropyMass : Nat" in lean
    assert "def NonPropRankEntropyWitnessFrontier" in lean
    assert "theorem bridge_soundness_from_nonPropRankEntropyWitness" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
    assert "axiom" not in lean


def test_nonprop_rank_entropy_witness_frontier_boundary_doc():
    doc = (ROOT / "docs/status/CHRONOS_NONPROP_RANK_ENTROPY_WITNESS_FRONTIER_2026_05_13.md").read_text()
    assert "FRONTIER_OPEN is preserved." in doc
    assert "This records the weakest missing non-Prop witness object only." in doc
    assert "No unrestricted UniversalFiberEntropyGap theorem is claimed." in doc
    assert "No Chronos-RR theorem closure is claimed." in doc
    assert "No H4.1/FGL closure is claimed." in doc
    assert "No P vs NP closure is claimed." in doc
    assert "No Clay-problem closure is claimed." in doc
