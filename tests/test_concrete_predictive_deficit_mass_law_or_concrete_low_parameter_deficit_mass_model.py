import subprocess
from pathlib import Path

def test_concrete_predictive_deficit_mass_law_or_concrete_low_parameter_deficit_mass_model_verifier():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_concrete_predictive_deficit_mass_law_or_concrete_low_parameter_deficit_mass_model.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "CONCRETE_PREDICTIVE_DEFICIT_MASS_LAW_OR_CONCRETE_LOW_PARAMETER_DEFICIT_MASS_MODEL_OK" in result.stdout
