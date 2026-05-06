from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "chronos" / "Certified" / "RepositoryNativeCertifiedDepth.lean"
STATUS = ROOT / "docs" / "status" / "CHRONOS_REPOSITORY_NATIVE_CERTIFIED_DEPTH_2026_05_06.md"
VERIFY = ROOT / "tools" / "verify_chronos_repository_native_certified_depth.py"

def test_no_placeholder_or_mathlib_tokens():
    text = LEAN.read_text()
    assert "import Mathlib" not in text
    assert "by sorry" not in text
    assert "admit" not in text
    assert "axiom " not in text
    assert "linarith" not in text
    assert "omega" not in text
    assert "ℚ" not in text

def test_repository_native_depth_is_carrier_annotation():
    text = LEAN.read_text()
    assert "I.depthAnnotation" in text
    assert "I.depthMinimum" in text
    assert "cert.depth" not in text
    assert "certificateDepth" not in text

def test_embedding_uses_backward_and_right_inverse():
    text = LEAN.read_text()
    assert "I.backward n x.query" in text
    assert "I.right_inv n x.query" in text

def test_rank_and_k_admissibility_are_explicit_inputs():
    text = LEAN.read_text()
    assert "hk : k = n ∨ k ≤ n" in text
    assert "hrn : n ≤ r" in text

def test_main_theorem_present():
    text = LEAN.read_text()
    assert "theorem RepositoryNativeCertifiedDepthLowerBound" in text
    assert "def RepositoryNativeDepthBridgeHypothesis" in text
    assert "theorem repositoryNativeDepthBridgeInstance" in text

def test_frontier_boundary_status():
    status = STATUS.read_text()
    assert "FRONTIER_OPEN" in status
    assert "Does not assert P vs NP closure" in status
    assert "Does not assert theorem-level Chronos closure" in status

def test_verifier_passes():
    subprocess.run(["python3", str(VERIFY)], cwd=ROOT, check=True)
