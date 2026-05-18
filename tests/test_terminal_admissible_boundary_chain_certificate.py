import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_terminal_admissible_boundary_chain_certificate_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_terminal_admissible_boundary_chain_certificate.py"],
        cwd=ROOT,
        check=True,
    )

def test_terminal_admissible_boundary_chain_certificate_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/terminal_admissible_boundary_chain_certificate_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "TERMINAL_ADMISSIBLE_BOUNDARY_CHAIN_CERTIFICATE_CLOSED_NO_THEOREM_PROMOTION"
    boundary = "\n".join(artifact["boundary"])
    assert "terminal admissible boundary-chain certificate only" in boundary
    assert "does not prove P vs NP" in boundary
    assert "does not refute P vs NP" in boundary
    assert "does not prove any Clay problem" in boundary
    assert "does not refute any Clay problem" in boundary

def test_terminal_admissible_boundary_chain_certificate_lean_surface_has_no_sorry():
    lean = (ROOT / "lean/Chronos/Frontier/TerminalAdmissibleBoundaryChainCertificate.lean").read_text()
    assert "theorem TerminalAdmissibleBoundaryChainCertificate_solved" in lean
    assert "theorem TerminalBoundaryChainAudit_solved" in lean
    assert "ClayStatus.frontier_open" in lean
    assert "PNPStatus.frontier_open" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
