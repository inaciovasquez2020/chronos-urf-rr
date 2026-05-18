import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_domain_indexed_positive_entropy_order_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_domain_indexed_positive_entropy_order.py"],
        cwd=ROOT,
        check=True,
    )

def test_domain_indexed_positive_entropy_order_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/domain_indexed_positive_entropy_order_2026_05_17.json").read_text()
    )
    assert artifact["status"] == "THEOREM_SURFACE_CLOSED_ORDER_THEORETIC_ONLY"
    boundary = "\n".join(artifact["boundary"])
    assert "does not prove unrestricted UniversalFiberEntropyGap" in boundary
    assert "does not prove P vs NP" in boundary
    assert "does not prove any Clay problem" in boundary

def test_domain_indexed_positive_entropy_order_lean_surface_has_no_sorry():
    lean = (ROOT / "lean/Chronos/Frontier/DomainIndexedPositiveEntropyOrder.lean").read_text()
    assert "theorem DomainIndexedPositiveEntropyWitnessConstruction_order_solved" in lean
    assert "theorem no_common_uniform_bound" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
