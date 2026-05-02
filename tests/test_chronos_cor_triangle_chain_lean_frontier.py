import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_chronos_cor_triangle_chain_lean_frontier_verifier_passes():
    subprocess.run(
        ["python3", "scripts/verify_chronos_cor_triangle_chain_lean_frontier.py"],
        cwd=ROOT,
        check=True,
    )

def test_chronos_cor_triangle_chain_boundary_doc_exists():
    doc = ROOT / "docs/status/CHRONOS_COR_TRIANGLE_CHAIN_LEAN_FRONTIER_2026_05_02.md"
    text = doc.read_text()
    assert "Lean theorem-frontier skeleton only" in text
    assert "It does not assert a Chronos closure theorem." in text
