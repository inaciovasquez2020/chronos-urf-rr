import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_semantic_rank_rate_coverage_realization_verifier():
    subprocess.run(
        ["python3", "tools/verify_semantic_rank_rate_coverage_realization.py"],
        cwd=ROOT,
        check=True,
    )

def test_semantic_rank_rate_coverage_realization_lean_surface():
    text = (ROOT / "Chronos/Frontier/SemanticRankRateCoverageRealization.lean").read_text()
    assert "structure SemanticRankRateCoverageRealization : Prop" in text
    assert "theorem semantic_rank_rate_coverage_realization_to_final_carrier_semantic_rank_rate_coverage" in text
    assert "FRONTIER_OPEN / REALIZATION_FRONTIER_ONLY" in text

def test_semantic_rank_rate_coverage_realization_doc_boundary():
    text = (ROOT / "docs/status/CHRONOS_SEMANTIC_RANK_RATE_COVERAGE_REALIZATION_2026_05_13.md").read_text()
    assert "No unrestricted UniversalFiberEntropyGap theorem." in text
    assert "No Chronos-RR." in text
    assert "No H4.1/FGL." in text
    assert "No P vs NP." in text
    assert "No Clay closure." in text
