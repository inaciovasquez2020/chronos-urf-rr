import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/gfe_polar_220_gr_darboux_certificate.json"
RECEIPT = ROOT / "artifacts/chronos/gfe_polar_220_gr_darboux_runtime_receipt.txt"
GENERATOR = ROOT / "tools/gfe/certify_gfe_polar_220_gr_darboux_root.sh"
SOURCE = ROOT / "artifacts/chronos/gfe_axial_220_projected_eft_certificate.json"

FORMULA_HASH = "8dd2a8896d9fedc9448f573c3d19c89483602a8396bcde061fdab8e31d8efcd6"
IDENTITY_HASH = "daed6d42a9594ca63a7efc014f645144af61b06a106253cc48851c5e6ee06f2c"
TRANSFER_HASH = "91ae286c3a37c0a742cf0e11201a7626527839dd334308310a8d7fc40016ee1a"


def load_record() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def test_exact_darboux_identities_and_hashes() -> None:
    record = load_record()
    assert record["schema"] == "chronos.gfe_polar_220_gr_darboux_certificate.v1"
    assert record["status"] == (
        "certified_gr_epsilon0_polar_220_root_via_exact_darboux_transfer"
    )
    assert all(record["darboux"]["identity_flags"].values())
    assert record["darboux"]["formula_hash"] == FORMULA_HASH
    assert record["darboux"]["identity_hash"] == IDENTITY_HASH


def test_source_axial_certificate_is_cryptographically_bound() -> None:
    record = load_record()
    assert record["source_axial_certificate"]["sha256"] == hashlib.sha256(
        SOURCE.read_bytes()
    ).hexdigest()
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert record["source_axial_certificate"]["matching_interval_newton_hash"] == (
        source["certificate_hashes"]["matching_interval_newton"]
    )


def test_unique_simple_polar_root_is_transferred_at_epsilon_zero() -> None:
    record = load_record()
    polar = record["polar_root_at_epsilon_0"]
    axial = json.loads(SOURCE.read_text(encoding="utf-8"))["root_tube"]
    assert polar["unique_simple_root"] is True
    assert polar["multiplicity_preserved"] is True
    assert polar["endpoint_conditions_preserved"] is True
    assert polar["same_disk_as_axial"] is True
    assert polar["disk_center"] == axial["omega_center_at_epsilon_0"]
    assert polar["disk_radius"] == axial["disk_radius"]
    assert polar["transfer_hash"] == TRANSFER_HASH


def test_root_disk_excludes_both_algebraically_special_frequencies() -> None:
    polar = load_record()["polar_root_at_epsilon_0"]
    assert polar["distance_to_plus_i_sigma_lower"] > 2.12
    assert polar["distance_to_minus_i_sigma_lower"] > 1.94
    assert polar["horizon_map_factor_abs_lower"] > 1.94
    assert polar["infinity_map_factor_abs_lower"] > 2.12
    assert polar["inverse_multiplier_abs_lower"] > 4.13


def test_runtime_receipt_and_executable_generator() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    required = {
        "ELL2_GR_DARBOUX_FACTORIZATION := certified",
        "ELL2_GR_DARBOUX_INTERTWINING := certified",
        "ELL2_GR_DARBOUX_WRONSKIAN_MULTIPLIER := certified",
        "ELL2_GR_DARBOUX_ENDPOINT_MAP := certified",
        f"ELL2_GR_DARBOUX_FORMULA_HASH := {FORMULA_HASH}",
        f"ELL2_GR_DARBOUX_IDENTITY_HASH := {IDENTITY_HASH}",
        f"ELL2_POLAR_GR_ROOT_TRANSFER_HASH := {TRANSFER_HASH}",
        "ELL2_POLAR_GR_UNIQUE_SIMPLE_ROOT := certified",
        "ELL2_POLAR_BETA2_ROOT_CONTINUATION := unproved",
    }
    assert required.issubset(set(receipt.splitlines()))
    assert GENERATOR.stat().st_mode & 0o111
    assert GENERATOR.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash")


def test_claim_boundary_preserves_actual_open_branch() -> None:
    record = load_record()
    boundary = "\n".join(record["claim_boundary"]).lower()
    assert record["scope"]["epsilon"] == 0.0
    assert record["scope"]["beta2_polar_correction"] is False
    assert "o(beta^2) polar quadratic action" in boundary
    assert "polar root continuation" in boundary
    assert "axial-polar splitting for epsilon>0" in boundary
    assert "unreduced trace-log" in boundary
    assert "massive mode" in boundary
