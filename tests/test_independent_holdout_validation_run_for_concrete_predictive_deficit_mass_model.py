import subprocess
from pathlib import Path

def test_independent_holdout_validation_run_for_concrete_predictive_deficit_mass_model_verifier():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_independent_holdout_validation_run_for_concrete_predictive_deficit_mass_model.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "INDEPENDENT_HOLDOUT_VALIDATION_RUN_FOR_CONCRETE_PREDICTIVE_DEFICIT_MASS_MODEL_OK" in result.stdout
