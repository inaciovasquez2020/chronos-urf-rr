import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_h4_1_fgl_selected_separating_observable_existence_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_selected_separating_observable_existence.py"],
        cwd=ROOT,
        check=True,
    )

def test_h4_1_fgl_selected_separating_observable_existence_artifact_boundary():
    data = json.loads(
        (ROOT / "artifacts/chronos/h4_1_fgl_selected_separating_observable_existence.json").read_text()
    )
    assert data["status"] == "SELECTED_INSTANCE_EXISTENCE_THEOREM"
    assert "H4_1_FGL_SelectedFinalCarrierSeparatingObservableExistence" in data["proves"]
    assert "left/right final-gap disjointness" in data["selected_instance_requires"]
    assert "separating observable existence for arbitrary semantic final carriers" in data["does_not_claim"]
    assert "P vs NP closure" in data["does_not_claim"]
