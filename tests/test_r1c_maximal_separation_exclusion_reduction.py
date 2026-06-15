import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/r1c_maximal_separation_exclusion_reduction_2026_06_15.json"
VERIFIER = ROOT / "tools/verify_r1c_maximal_separation_exclusion_reduction.py"


def test_r1c_maximal_separation_exclusion_reduction_verifies():
    result = subprocess.run(
        ["python3", str(VERIFIER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R1C_MAXIMAL_SEPARATION_EXCLUSION_REDUCTION_OK" in result.stdout


def test_r1c_maximal_separation_exclusion_reduction_rejects_overclaim(tmp_path):
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    data["boundary"]["proof_claims"]["proves_r1c"] = True
    bad_artifact = tmp_path / "bad_r1c_reduction.json"
    bad_artifact.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

    result = subprocess.run(
        ["python3", str(VERIFIER), str(bad_artifact)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "overclaiming proof flag: proves_r1c" in result.stderr


def test_r1c_maximal_separation_exclusion_reduction_rejects_missing_strict_bound(tmp_path):
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    data["exact_statement"]["hypotheses"].remove("LocalPatchDiameterBound(I,w) < D_i")
    bad_artifact = tmp_path / "bad_r1c_no_strict_bound.json"
    bad_artifact.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

    result = subprocess.run(
        ["python3", str(VERIFIER), str(bad_artifact)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "missing hypothesis: LocalPatchDiameterBound(I,w) < D_i" in result.stderr
