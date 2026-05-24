import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_large_scale_finite_capacity_optical_metric_sweep_values():
    proc = subprocess.run(
        [
            "python3",
            "tools/run_finite_capacity_optical_metric_large_scale_sweep.py",
            "--json",
        ],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    data = json.loads(proc.stdout)

    assert data["eps"] == 0.5
    assert data["R"] == 10.0
    assert data["r_min"] == 0.0
    assert data["r_max"] == 100.0
    assert data["samples"] == 10001

    assert data["passed"] is True
    assert data["n_strictly_increases"] is True
    assert data["alpha_strictly_decreases"] is True
    assert data["dn_dr_positive"] is True
    assert data["dalpha_dr_negative"] is True
    assert data["alpha_bounded_by_4"] is True

    assert abs(data["n_min"] - 0.5) < 1e-15
    assert 0.9999 < data["n_max"] < 1.0
    assert 1.0 < data["alpha_min"] < 1.001
    assert abs(data["alpha_max"] - 4.0) < 1e-15
    assert data["min_dn_dr"] > 0.0
    assert data["max_dn_dr"] == 0.05
    assert data["min_dalpha_dr"] == -0.8
    assert data["max_dalpha_dr"] < 0.0
