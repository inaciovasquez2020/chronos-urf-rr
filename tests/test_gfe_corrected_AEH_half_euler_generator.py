from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools/gfe/derive_gfe_corrected_euler_generator.py"
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"
SOURCE = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_full_lagrangian.json"


def test_rebuild_and_exact_descriptor_surface() -> None:
    before = ARTIFACT.read_bytes()
    run = subprocess.run(
        ["python3", str(GENERATOR)], cwd=ROOT, check=True,
        capture_output=True, text=True, timeout=180,
    )
    assert "EULER_FROM_ACTION := passed" in run.stdout
    assert "H0R2_COEFFICIENT := 3" in run.stdout
    assert ARTIFACT.read_bytes() == before

    data = json.loads(before)
    assert data["source_action_sha256"] == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert data["euler_from_action"] == [True, True]
    assert data["differential_orders"] == {
        "E0_h0": 4, "E0_h1": 3, "E1_h0": 3, "E1_h1": 2,
    }
    assert data["state_dimension"] == 6
    assert data["gr_reduction"] == [True, True]

    payload_hash = data.pop("payload_sha256")
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(encoded).hexdigest() == payload_hash

    beta, lam, omega = sp.symbols("beta lam omega")
    det = sp.sympify(data["descriptor_determinant"], locals={
        "beta": beta, "lam": lam, "omega": omega,
    })
    assert det != 0
    assert sp.simplify(det.subs(beta, 0)) == 0
    assert sp.simplify(det.subs(omega, 0)) == 0


def test_obsolete_normalization_is_absent() -> None:
    data = json.loads(ARTIFACT.read_text())
    assert "AEH=1/2" in data["scope"]
    source = json.loads(SOURCE.read_text())
    assert source["gates"]["coeff_h0_r_squared_beta0_lambda6"] == "3"
