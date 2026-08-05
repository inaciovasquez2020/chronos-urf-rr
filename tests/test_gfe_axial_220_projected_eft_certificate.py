import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/gfe_axial_220_projected_eft_certificate.json"
RECEIPT = ROOT / "artifacts/chronos/gfe_axial_220_projected_eft_runtime_receipt.txt"
GENERATOR = ROOT / "tools/gfe/derive_gfe_axial_quadratic_action.sh"


def load_record() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def receipt_text() -> str:
    return RECEIPT.read_text(encoding="utf-8")


def test_projected_axial_certificate_scope_and_hashes() -> None:
    record = load_record()
    assert record["schema"] == "chronos.gfe_axial_220_projected_eft_certificate.v1"
    assert record["scope"]["branch"] == "projected massless order-reduced EFT"
    assert record["scope"]["unreduced_trace_log_spectrum"] is False
    hashes = record["certificate_hashes"]
    assert hashes["canonical_potential"] == (
        "f21171a9b410fc311832fca2c55e363d90066f0872cbb19dab2e38f2434e5a94"
    )
    assert hashes["matching_interval_newton"] == (
        "756292809ddc9638d045ecdff723896cc38d02a87e02f1581e31ed24353d6147"
    )
    assert hashes["epsilon0_tangent_propagation"] == (
        "505622d2e96a94d41891f09ad623ca66d0cfa11f4ef4561c4051a96a8356f8ef"
    )


def test_unique_simple_root_tube_and_derivative_sign() -> None:
    record = load_record()
    root = record["root_tube"]
    derivative = record["implicit_derivative_at_epsilon_0"]
    assert root["unique_simple_root_for_each_epsilon"] is True
    assert 0 < root["disk_radius"] < 1e-5
    assert derivative["D_Omega_nonzero"] is True
    assert derivative["real_part_positive"] is True
    assert derivative["real_lower_bound"] > 0
    assert derivative["center"][0] - derivative["disk_radius"] > 0


def test_runtime_receipt_contains_terminal_certificates() -> None:
    receipt = receipt_text()
    required_lines = (
        "ELL2_BETA2_CANONICAL_POTENTIAL_HASH := "
        "f21171a9b410fc311832fca2c55e363d90066f0872cbb19dab2e38f2434e5a94",
        "ELL2_AXIAL_MATCHING_HASH := "
        "756292809ddc9638d045ecdff723896cc38d02a87e02f1581e31ed24353d6147",
        "ELL2_AXIAL_EPSILON0_TANGENT_HASH := "
        "4d4a1a28d2320c66eee4456622fd175f288f6fa93ba716d44d6feb686b88b81a",
        "ELL2_AXIAL_EPSILON0_ENDPOINT_TANGENT_HASH := "
        "94ec87296b933bf4de3aada5d8bede67a80619f0767410e82767d64d5239d8c1",
        "ELL2_AXIAL_EPSILON0_TANGENT_PROPAGATION_HASH := "
        "505622d2e96a94d41891f09ad623ca66d0cfa11f4ef4561c4051a96a8356f8ef",
        "ELL2_AXIAL_MATCHING_INTERVAL_NEWTON := certified",
        "ELL2_AXIAL_MATCHING_UNIQUE_SIMPLE_ROOT_TUBE := certified",
        "ELL2_AXIAL_MATCHING_EPSILON_INTERVAL := [0,1/10000]",
        "ELL2_AXIAL_MATCHING_NEWTON_DISK_RADIUS := 1/150000",
        "ELL2_AXIAL_EPSILON0_RICCATI_TANGENT_SYSTEM := certified",
        "ELL2_AXIAL_EPSILON0_IMPLICIT_DERIVATIVE_FORMULA := certified",
        "ELL2_AXIAL_EPSILON0_ENDPOINT_TANGENTS := certified",
        "ELL2_AXIAL_EPSILON0_HORIZON_ENDPOINT_TANGENTS := certified",
        "ELL2_AXIAL_EPSILON0_INFINITY_ENDPOINT_TANGENTS := certified",
        "ELL2_AXIAL_EPSILON0_CENTER_Q_REFINEMENT := certified",
        "ELL2_AXIAL_EPSILON0_TANGENT_PROPAGATION := certified",
        "ELL2_AXIAL_EPSILON0_IMPLICIT_DERIVATIVE := certified",
    )
    lines = set(receipt.splitlines())
    for line in required_lines:
        assert line in lines


def test_generator_is_executable_shell_source() -> None:
    source = GENERATOR.read_text(encoding="utf-8")
    assert source.startswith("#!/usr/bin/env bash") or source.startswith("#!/bin/bash")
    assert GENERATOR.stat().st_mode & 0o111


def test_claim_boundary_preserves_open_polar_and_unreduced_branches() -> None:
    boundary = "\n".join(load_record()["claim_boundary"]).lower()
    assert "polar" in boundary
    assert "axial-polar splitting" in boundary
    assert "unreduced trace-log" in boundary
    assert "massive mode" in boundary
