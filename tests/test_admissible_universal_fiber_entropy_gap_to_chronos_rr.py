import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_admissible_universal_fiber_entropy_gap_to_chronos_rr_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_admissible_universal_fiber_entropy_gap_to_chronos_rr.py"],
        cwd=ROOT,
        check=True,
    )

def test_admissible_universal_fiber_entropy_gap_to_chronos_rr_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/admissible_universal_fiber_entropy_gap_to_chronos_rr_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "ADMISSIBLE_CHRONOS_RR_TARGET_CLOSED_RESTRICTED_ONLY"
    boundary = "\n".join(artifact["boundary"])
    assert "admissible restricted Chronos-RR target only" in boundary
    assert "does not prove unrestricted Chronos-RR" in boundary
    assert "does not prove P vs NP" in boundary

def test_admissible_universal_fiber_entropy_gap_to_chronos_rr_lean_surface_has_no_sorry():
    lean = (ROOT / "lean/Chronos/Frontier/AdmissibleUniversalFiberEntropyGapToChronosRR.lean").read_text()
    assert "theorem AdmissibleUniversalFiberEntropyGapToChronosRR_solved" in lean
    assert "theorem AdmissibleChronosRRTarget_solved" in lean
    assert "theorem UnrestrictedChronosRRTarget_refuted" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
