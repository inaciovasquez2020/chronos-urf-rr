import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_admissible_rate_thick_to_universal_fiber_entropy_gap_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_admissible_rate_thick_to_universal_fiber_entropy_gap.py"],
        cwd=ROOT,
        check=True,
    )

def test_admissible_rate_thick_to_universal_fiber_entropy_gap_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/admissible_rate_thick_to_universal_fiber_entropy_gap_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "ADMISSIBLE_UNIVERSAL_FIBER_ENTROPY_GAP_TARGET_CLOSED_RESTRICTED_ONLY"
    boundary = "\n".join(artifact["boundary"])
    assert "admissible restricted universal fiber-entropy gap target only" in boundary
    assert "does not prove unrestricted UniversalFiberEntropyGap" in boundary
    assert "does not prove P vs NP" in boundary

def test_admissible_rate_thick_to_universal_fiber_entropy_gap_lean_surface_has_no_sorry():
    lean = (ROOT / "lean/Chronos/Frontier/AdmissibleRateThickToUniversalFiberEntropyGap.lean").read_text()
    assert "theorem AdmissibleRateThickFiberCoercivityToUniversalFiberEntropyGap_solved" in lean
    assert "theorem AdmissibleUniversalFiberEntropyGapTarget_solved" in lean
    assert "theorem UnrestrictedUniversalFiberEntropyGapTarget_refuted" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
