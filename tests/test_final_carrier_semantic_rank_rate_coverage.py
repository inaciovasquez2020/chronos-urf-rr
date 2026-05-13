import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_final_carrier_semantic_rank_rate_coverage_verifier():
    subprocess.run(
        ["python3", "tools/verify_final_carrier_semantic_rank_rate_coverage.py"],
        cwd=ROOT,
        check=True,
    )

def test_final_carrier_semantic_rank_rate_coverage_lean_surface():
    text = (ROOT / "Chronos/Frontier/FinalCarrierSemanticRankRateCoverage.lean").read_text()
    assert "structure FinalCarrierSemanticRankRateCoverage : Prop" in text
    assert "theorem final_carrier_semantic_rank_rate_coverage_to_universal_fiber_entropy_gap" in text
    assert "FRONTIER_OPEN / COVERAGE_FRONTIER_ONLY" in text

def test_final_carrier_semantic_rank_rate_coverage_doc_boundary():
    text = (ROOT / "docs/status/CHRONOS_FINAL_CARRIER_SEMANTIC_RANK_RATE_COVERAGE_2026_05_13.md").read_text()
    assert "No unrestricted UniversalFiberEntropyGap theorem." in text
    assert "No Chronos-RR." in text
    assert "No H4.1/FGL." in text
    assert "No P vs NP." in text
    assert "No Clay closure." in text
