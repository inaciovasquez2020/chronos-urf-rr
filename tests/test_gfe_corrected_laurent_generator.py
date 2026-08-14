from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "tools/gfe/derive_gfe_corrected_laurent_generator.py"
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_laurent_generator.json"
DESCRIPTOR = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"


def test_deterministic_exact_laurent_export() -> None:
    before = ARTIFACT.read_bytes()
    run = subprocess.run(
        ["python3", str(EXPORTER)], cwd=ROOT, check=True,
        capture_output=True, text=True, timeout=180,
    )
    assert "GENERATOR_MIN_LAURENT_ORDER := -1" in run.stdout
    assert "EXACT_EG_EQUALS_A := passed" in run.stdout
    assert ARTIFACT.read_bytes() == before


def test_exact_certificate_boundary_and_hash() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert data["certificate"] == "GFE_CORRECTED_AEH_HALF_GUARDED_LAURENT_GENERATOR"
    assert data["source_descriptor_sha256"] == hashlib.sha256(DESCRIPTOR.read_bytes()).hexdigest()
    assert data["descriptor_determinant_beta_valuation"] == 3
    assert data["global_adjugate_A_beta_valuation"] == 2
    assert data["generator_minimum_laurent_order"] == -1
    assert data["principal_part_range"] == [-1, -1]
    assert data["ordinary_generator_guard"] == json.loads(
        DESCRIPTOR.read_text(encoding="utf-8"))["ordinary_generator_guard"]
    assert all(data["exact_checks"].values())
    payload_hash = data.pop("payload_sha256")
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(encoded).hexdigest() == payload_hash


def test_all_orders_rule_and_coefficients_through_G1() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    M, r, lam, omega = sp.symbols("M r lam omega")
    local = {"M": M, "r": r, "lam": lam, "omega": omega, "I": sp.I}
    numerator = data["reduced_numerator_beta_coefficients"]
    denominator = [sp.sympify(x, locals=local)
                   for x in data["regular_denominator_beta_coefficients"]]
    assert sp.cancel(denominator[0]) != 0
    inverse = [1 / denominator[0]]
    for n in range(1, 3):
        inverse.append(sp.cancel(-sum(
            denominator[j] * inverse[n-j]
            for j in range(1, min(n, len(denominator) - 1) + 1)
        ) / denominator[0]))
    for exponent, name in ((-1, "G_-1"), (0, "G_0"), (1, "G_1")):
        exported = data["laurent_coefficients"][name]
        for i in range(6):
            for j in range(6):
                expected = 0
                for degree in range(min(len(numerator) - 1, exponent + 1) + 1):
                    expected += sp.sympify(numerator[degree][i][j], locals=local) * inverse[exponent + 1 - degree]
                assert sp.cancel(sp.sympify(exported[i][j], locals=local) - expected) == 0
    assert any(sp.sympify(x, locals=local) != 0
               for row in data["laurent_coefficients"]["G_-1"] for x in row)
