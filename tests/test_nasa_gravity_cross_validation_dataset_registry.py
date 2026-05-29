import json
import subprocess
from pathlib import Path

def test_nasa_gravity_cross_validation_dataset_registry():
    result = subprocess.run(
        ["python3", "tools/verify_nasa_gravity_cross_validation_dataset_registry.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_OK" in result.stdout

    artifact = Path("artifacts/gravity/nasa_gravity_cross_validation_dataset_registry_2026_05_29.json")
    payload = json.loads(artifact.read_text())

    assert payload["status"] == "NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_CREATED"
    assert payload["dataset_count"] == 12
    assert len(payload["datasets"]) == 12
    assert len(payload["required_next_payload_gates"]) == 11

    names = {d["short_name"] for d in payload["datasets"]}
    assert "GRACEFO_L2_JPL_MONTHLY_0063" in names
    assert "TELLUS_GRAC-GRFO_MASCON_GRID_RL06.3_V4" in names
    assert "GRC-GFO_GRIDDED_AOD1B_JPL_MASCON_RL06.3" in names
    assert "GLDAS_NOAH025_3H_2.1" in names
    assert "SPL4SMGP.008" in names
    assert "ATL06.007" in names
    assert "SWOT_L2_HR_RiverSP_2.0" in names
    assert "GPM_3IMERGDF.07" in names
    assert "NASA_LAMBDA_CMB_PRODUCTS" in names
