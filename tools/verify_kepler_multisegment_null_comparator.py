#!/usr/bin/env python3
import importlib.util
import json
import math
import sys
from pathlib import Path


REQUIRED_NON_CLAIMS = {
    "gravity closure",
    "cosmology closure",
    "Chronos-RR closure",
    "physical time theorem closure",
    "ZeroDay closure",
}

FORBIDDEN_PROMOTIONS = [
    "GravityClosure",
    "CosmologyClosure",
    "ChronosRR",
    "H41_FGL",
    "ZeroDayClosure",
    "PhysicalTimeTheorem",
]

FORBIDDEN_OUTPUTS = [
    "PLANET_DETECTED",
    "PHYSICAL_TIME_CONFIRMED",
    "CHRONOS_OBSERVABLE_CONFIRMED",
    "GRAVITY_MODEL_VALIDATED",
    "COSMOLOGY_VALIDATED",
]

ALLOWED_OUTPUT = "FINITE_LIGHT_CURVE_SEGMENTS_COMPARED_TO_CONSTANT_NULL"
ALLOWED_SELECTION_RULE = "first_verified_interval_from_receipt_then_first_later_non_overlapping_finite_window_of_equal_length"


def fail(message):
    print(f"ERROR: {message}")
    raise SystemExit(1)


def load_json(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception as exc:
        fail(f"Could not load JSON {path}: {exc}")


def load_semantic_module():
    verifier_path = Path("tools/verify_kepler_fits_semantic_predicate.py")
    if not verifier_path.exists():
        fail("MISSING_OBJECT := tools/verify_kepler_fits_semantic_predicate.py")
    spec = importlib.util.spec_from_file_location("kepler_semantic_verifier", verifier_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_boundaries(*objects):
    raw_text = json.dumps(objects, sort_keys=True)
    for token in FORBIDDEN_PROMOTIONS:
        if token in raw_text:
            fail(f"Anti-promotion guard triggered. Forbidden term '{token}' identified.")

    found = set()
    for obj in objects:
        found |= set(obj.get("non_claims", []))
    if not REQUIRED_NON_CLAIMS.issubset(found):
        fail("Missing mandatory closure non-claims.")


def non_overlapping(a, b):
    return int(a["end_row"]) < int(b["start_row"]) or int(b["end_row"]) < int(a["start_row"])


def verify_interval(module, fits_path, table, column_name, start_row, end_row):
    return module.extract_column_interval(fits_path, table, column_name, start_row, end_row)


def comparator(values):
    mean = sum(values) / len(values)
    mean_abs_residual = sum(abs(value - mean) for value in values) / len(values)
    if not math.isfinite(mean) or not math.isfinite(mean_abs_residual):
        fail("Comparator produced non-finite statistic.")
    return mean, mean_abs_residual


def verify(receipt_path, rollup_path, multisegment_path, anti_overfit_path):
    receipt_path = Path(receipt_path)
    rollup = load_json(rollup_path)
    multisegment = load_json(multisegment_path)
    anti_overfit = load_json(anti_overfit_path)
    receipt = load_json(receipt_path)

    check_boundaries(receipt, rollup, multisegment, anti_overfit)

    if receipt.get("receipt_class") != "PINNED_MAST_FITS_EVIDENCE":
        fail("Multi-segment verification requires PINNED_MAST_FITS_EVIDENCE.")

    if multisegment.get("allowed_output") != ALLOWED_OUTPUT:
        fail("Invalid multi-segment allowed_output.")

    if multisegment.get("segment_selection_rule") != ALLOWED_SELECTION_RULE:
        fail("Invalid or adaptive segment selection rule.")

    if anti_overfit.get("allowed_selection_rule") != ALLOWED_SELECTION_RULE:
        fail("Anti-overfitting receipt does not bind the allowed deterministic selection rule.")

    fits_path = receipt_path.parent / receipt.get("filename", "")
    if not fits_path.exists():
        fail(f"MISSING_OBJECT := {fits_path}")

    module = load_semantic_module()
    actual_hash = module.sha256_file(fits_path)
    if actual_hash != receipt.get("sha256"):
        fail(f"FITS SHA-256 mismatch. Expected {receipt.get('sha256')}, got {actual_hash}")

    time_column = multisegment.get("time_column")
    flux_column = multisegment.get("flux_column")
    if time_column != receipt.get("time_column"):
        fail("Multisegment time_column does not match receipt.")
    if flux_column != receipt.get("flux_column"):
        fail("Multisegment flux_column does not match receipt.")
    if flux_column != "PDCSAP_FLUX":
        fail("Multi-segment comparator is bound to PDCSAP_FLUX.")

    table = module.find_binary_table_with_columns(fits_path, {time_column, flux_column})

    segments = multisegment.get("segments", [])
    if len(segments) != 2:
        fail("Expected exactly two finite light-curve segments.")

    intervals = [segment.get("interval_rows", {}) for segment in segments]
    if not non_overlapping(intervals[0], intervals[1]):
        fail("Segments must be non-overlapping.")

    expected_first = receipt.get("finite_interval")
    if intervals[0] != expected_first:
        fail("First multisegment interval must equal receipt finite_interval.")

    stats = []
    for segment in segments:
        if segment.get("null_comparator") != "constant_flux_mean_residual":
            fail("Only constant_flux_mean_residual is allowed.")
        interval = segment["interval_rows"]
        start_row = int(interval["start_row"])
        end_row = int(interval["end_row"])
        time_values = verify_interval(module, fits_path, table, time_column, start_row, end_row)
        flux_values = verify_interval(module, fits_path, table, flux_column, start_row, end_row)

        if len(time_values) != len(flux_values):
            fail("TIME and PDCSAP_FLUX interval lengths differ.")
        if len(flux_values) == 0:
            fail("Empty segment interval.")

        mean_flux, mean_abs_residual = comparator(flux_values)
        stats.append((segment["segment_id"], start_row, end_row, mean_flux, mean_abs_residual))

    print("KEPLER_MULTISEGMENT_NULL_COMPARATOR_OK")
    for segment_id, start_row, end_row, mean_flux, mean_abs_residual in stats:
        print(f"SEGMENT := {segment_id}")
        print(f"ROWS_VERIFIED := {start_row}..{end_row}")
        print(f"MEAN_FLUX := {mean_flux:.12g}")
        print(f"MEAN_ABS_RESIDUAL := {mean_abs_residual:.12g}")
    print("BOUNDARY := no gravity/cosmology/Chronos-RR/physical-time/ZeroDay closure")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        fail(
            "Usage: verify_kepler_multisegment_null_comparator.py "
            "<receipt.json> <rollup.json> <multisegment.json> <anti_overfitting.json>"
        )
    verify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
