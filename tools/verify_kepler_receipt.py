#!/usr/bin/env python3
import hashlib
import json
import os
import sys


EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def calculate_local_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as handle:
        for byte_block in iter(lambda: handle.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def fail(message):
    print(f"ERROR: {message}")
    sys.exit(1)


def verify_receipt(receipt_path):
    try:
        with open(receipt_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        fail(f"Failed to parse receipt file: {exc}")

    receipt_class = data.get("receipt_class")
    allowed_receipt_classes = {"STRUCTURAL_STUB_ONLY", "PINNED_MAST_FITS_EVIDENCE"}
    if receipt_class not in allowed_receipt_classes:
        fail(f"Invalid receipt_class: {receipt_class}")

    required_non_claims = {
        "gravity closure",
        "cosmology closure",
        "Chronos-RR closure",
        "physical time theorem closure",
        "ZeroDay closure",
    }
    current_non_claims = set(data.get("non_claims", []))
    if not required_non_claims.issubset(current_non_claims):
        fail("Receipt lacks mandatory negative-boundary certificates.")

    forbidden_promotions = [
        "GravityClosure",
        "CosmologyClosure",
        "ChronosRR",
        "H41_FGL",
        "ZeroDayClosure",
        "PhysicalTimeTheorem",
    ]
    raw_text = json.dumps(data, sort_keys=True)
    for term in forbidden_promotions:
        if term in raw_text:
            fail(f"Anti-promotion guard triggered. Forbidden term '{term}' identified.")

    allowed_output = "FINITE_LIGHT_CURVE_SEGMENT_COMPARED_TO_CONSTANT_NULL"
    actual_output = data.get("null_comparator_output")
    if actual_output != allowed_output:
        fail(f"Non-compliant comparator output: {actual_output}")

    forbidden_outputs = [
        "PLANET_DETECTED",
        "PHYSICAL_TIME_CONFIRMED",
        "CHRONOS_OBSERVABLE_CONFIRMED",
        "GRAVITY_MODEL_VALIDATED",
        "COSMOLOGY_VALIDATED",
    ]
    for forbidden_output in forbidden_outputs:
        if forbidden_output in raw_text:
            fail(f"Prohibited high-level inference token detected: {forbidden_output}")

    target_filename = data.get("filename")
    expected_hash = data.get("sha256")
    local_dir = os.path.dirname(receipt_path)
    potential_local_file = os.path.join(local_dir, target_filename)

    if receipt_class == "PINNED_MAST_FITS_EVIDENCE" and expected_hash == EMPTY_SHA256:
        fail("PINNED_MAST_FITS_EVIDENCE requires a non-empty SHA-256 digest.")

    if os.path.exists(potential_local_file):
        actual_hash = calculate_local_sha256(potential_local_file)
        if actual_hash == EMPTY_SHA256:
            if receipt_class != "STRUCTURAL_STUB_ONLY":
                fail("Zero-byte local file requires receipt_class=STRUCTURAL_STUB_ONLY.")
            print(f"NOTICE: Structural stub detected for {target_filename}; no observational evidence pin is claimed.")
        elif receipt_class == "PINNED_MAST_FITS_EVIDENCE" and actual_hash != expected_hash:
            fail(f"Cryptographic mismatch for local file artifact. Expected: {expected_hash}, Got: {actual_hash}")
        elif receipt_class == "STRUCTURAL_STUB_ONLY":
            print(f"NOTICE: Local non-empty file present for {target_filename}, but receipt remains STRUCTURAL_STUB_ONLY.")
        else:
            print(f"SUCCESS: Local asset cryptographic parity confirmed for {target_filename}.")
    else:
        if receipt_class == "PINNED_MAST_FITS_EVIDENCE":
            fail("PINNED_MAST_FITS_EVIDENCE requires the local FITS artifact to be present.")
        print("NOTICE: Physical binary asset missing. Proceeding with STRUCTURAL_STUB_ONLY metadata validation.")

    print(f"SUCCESS: {receipt_path} structural boundaries verified.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("Usage: verify_kepler_receipt.py <path_to_receipt>")
    verify_receipt(sys.argv[1])
