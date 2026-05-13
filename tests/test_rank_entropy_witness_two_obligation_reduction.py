import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_rank_entropy_witness_two_obligation_reduction_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_rank_entropy_witness_two_obligation_reduction.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "RankEntropyWitness two-obligation reduction verified." in result.stdout


def test_rank_entropy_witness_two_obligation_reduction_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/rank_entropy_witness_two_obligation_reduction_2026_05_13.json").read_text()
    )
    assert data["status"] == "FRONTIER_OPEN / TWO_OBLIGATION_REDUCTION_ONLY"
    assert data["frontier_open_preserved"] is True
    assert data["theorem_level_closure"] is False
    assert data["remaining_obligations"] == [
        "LiveRankEntropyWitnessSelector",
        "RankEntropyWitnessBridgeLaw",
    ]


def test_rank_entropy_witness_two_obligation_reduction_lean_tokens():
    lean = (ROOT / "Chronos/Frontier/RankEntropyWitnessTwoObligationReduction.lean").read_text()
    assert "def LiveRankEntropyWitnessSelector" in lean
    assert "def RankEntropyWitnessBridgeLaw" in lean
    assert "theorem nonPropRankEntropyWitnessFrontier_from_selector_and_bridge" in lean
    assert "theorem semanticRankRateToFiberEntropySoundness_from_selector_and_bridge" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
    assert "axiom" not in lean


def test_rank_entropy_witness_two_obligation_reduction_boundary_doc():
    doc = (ROOT / "docs/status/CHRONOS_RANK_ENTROPY_WITNESS_TWO_OBLIGATION_REDUCTION_2026_05_13.md").read_text()
    assert "FRONTIER_OPEN is preserved." in doc
    assert "This is a two-obligation reduction only." in doc
    assert "No LiveRankEntropyWitnessSelector theorem is claimed." in doc
    assert "No RankEntropyWitnessBridgeLaw theorem is claimed." in doc
    assert "No unrestricted UniversalFiberEntropyGap theorem is claimed." in doc
    assert "No Chronos-RR theorem closure is claimed." in doc
    assert "No H4.1/FGL closure is claimed." in doc
    assert "No P vs NP closure is claimed." in doc
    assert "No Clay-problem closure is claimed." in doc
