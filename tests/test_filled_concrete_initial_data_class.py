import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_filled_concrete_initial_data_class_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_filled_concrete_initial_data_class.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "FILLED_CONCRETE_INITIAL_DATA_CLASS_ONLY_NO_ANALYTIC_ESTIMATE_PROOF" in result.stdout

def test_filled_concrete_initial_data_class_artifact_boundaries():
    data = json.loads((ROOT / "artifacts/chronos/filled_concrete_initial_data_class_2026_05_23.json").read_text())
    assert data["next_admissible_object"] == "ConcreteConstraintCompatibilityCertificate"
    assert "P vs NP" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
