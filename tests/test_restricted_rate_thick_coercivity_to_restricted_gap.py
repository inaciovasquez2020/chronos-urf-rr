from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_restricted_rate_thick_coercivity_to_restricted_gap.py"],
        cwd=ROOT,
        check=True,
    )

def test_artifact_status_and_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/restricted_rate_thick_coercivity_to_restricted_universal_fiber_entropy_gap_2026_05_18.json").read_text()
    )
    assert artifact["target"] == "RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap"
    assert artifact["status"] == "RESTRICTED_RATE_THICK_COERCIVITY_TO_RESTRICTED_GAP_CLOSED"
    boundary = "\n".join(artifact["boundary"])
    assert "restricted-domain bridge only" in boundary
    assert "finite-support measure package only" in boundary
    assert "unrestricted UniversalFiberEntropyGap remains FRONTIER_OPEN" in boundary
    assert "no unrestricted UniversalFiberEntropyGap" in boundary
    assert "no Clay-problem closure" in boundary

def test_lean_surface_contains_restricted_bridge_only():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap.lean").read_text()
    assert "structure RestrictedUniversalFiberEntropyGap" in text
    assert "def RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap" in text
    assert "restricted_rate_thick_coercivity_to_restricted_gap_closed" in text
    assert "unrestricted_universal_fiber_entropy_gap_frontier_open" in text
    assert "def UniversalFiberEntropyGap" not in text
    assert "structure UniversalFiberEntropyGap" not in text
    assert "admit" not in text
    assert "sorry" not in text
    assert "axiom" not in text
