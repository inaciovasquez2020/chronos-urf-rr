import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/r1b_f2_linear_combination_no_new_long_chord_reduction_2026_06_15.json"
VERIFIER = ROOT / "tools/verify_r1b_f2_linear_combination_no_new_long_chord_reduction.py"


def test_r1b_f2_linear_combination_reduction_verifies():
    result = subprocess.run(
        ["python3", str(VERIFIER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R1B_F2_LINEAR_COMBINATION_REDUCTION_OK" in result.stdout


def test_r1b_f2_linear_combination_reduction_rejects_overclaim(tmp_path):
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    data["boundary"]["proof_claims"]["proves_r1"] = True
    bad_artifact = tmp_path / "bad_r1b_reduction.json"
    bad_artifact.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

    result = subprocess.run(
        ["python3", str(VERIFIER), str(bad_artifact)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "overclaiming proof flag: proves_r1" in result.stderr


def test_r1b_f2_linear_combination_reduction_requires_r1a_conditional(tmp_path):
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    data["discharged_subclaim"]["conditional_on"] = [
        item for item in data["discharged_subclaim"]["conditional_on"]
        if item != "R1a generator-level absence for each trivial 2-face boundary"
    ]
    bad_artifact = tmp_path / "bad_r1b_missing_r1a.json"
    bad_artifact.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

    result = subprocess.run(
        ["python3", str(VERIFIER), str(bad_artifact)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "missing R1a conditional" in result.stderr
