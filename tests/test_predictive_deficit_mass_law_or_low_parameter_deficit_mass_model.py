import subprocess
from pathlib import Path

def test_predictive_deficit_mass_law_or_low_parameter_deficit_mass_model_verifier():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_predictive_deficit_mass_law_or_low_parameter_deficit_mass_model.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "PREDICTIVE_DEFICIT_MASS_LAW_OR_LOW_PARAMETER_DEFICIT_MASS_MODEL_OK" in result.stdout
