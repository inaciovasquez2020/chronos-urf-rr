#!/usr/bin/env python3
import importlib.util
import json
import math
import statistics
import struct
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

ALLOWED_OUTPUT = "FINITE_LIGHT_CURVE_ALL_WINDOWS_COMPARED_TO_CONSTANT_NULL"
WINDOW_LENGTH = 100
SELECTION_RULE = "scan_all_contiguous_100_row_windows_and_keep_only_finite_TIME_PDCSAP_FLUX_windows"


def fail(message):
    print(f"ERROR: {message}")
    raise SystemExit(1)


def load_json(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception as exc:
        fail(f"Could not load JSON {path}: {exc}")


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2) + "\n")


def load_semantic_module():
    path = Path("tools/verify_kepler_fits_semantic_predicate.py")
    if not path.exists():
        fail("MISSING_OBJECT := tools/verify_kepler_fits_semantic_predicate.py")
    spec = importlib.util.spec_from_file_location("kepler_semantic_verifier", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def boundary_check(*objects):
    raw_text = json.dumps(objects, sort_keys=True)
    for token in FORBIDDEN_PROMOTIONS:
        if token in raw_text:
            fail(f"Anti-promotion guard triggered. Forbidden term '{token}' identified.")

    found = set()
    for obj in objects:
        found |= set(obj.get("non_claims", []))
    if not REQUIRED_NON_CLAIMS.issubset(found):
        fail("Missing mandatory closure non-claims.")


def read_scalar(raw, code):
    if code == "E":
        return struct.unpack(">f", raw[:4])[0]
    if code == "D":
        return struct.unpack(">d", raw[:8])[0]
    if code == "J":
        return float(struct.unpack(">i", raw[:4])[0])
    if code == "I":
        return float(struct.unpack(">h", raw[:2])[0])
    if code == "K":
        return float(struct.unpack(">q", raw[:8])[0])
    if code == "B":
        return float(raw[0])
    fail(f"Cannot read scalar for FITS code: {code}")


def read_value(handle, table, column, row_number):
    row_offset = table["data_start"] + (row_number - 1) * table["row_len"]
    handle.seek(row_offset + column["offset"])
    raw = handle.read(column["size"])
    if len(raw) != column["size"]:
        fail(f"Could not read complete value at row {row_number}.")
    return read_scalar(raw, column["code"])


def constant_flux_mean_abs_residual(values):
    mean_flux = sum(values) / len(values)
    mean_abs_residual = sum(abs(value - mean_flux) for value in values) / len(values)
    if not math.isfinite(mean_flux) or not math.isfinite(mean_abs_residual):
        fail("Comparator produced non-finite statistic.")
    return mean_flux, mean_abs_residual


def scan_windows(fits_path, table):
    time_column = table["columns"]["TIME"]
    flux_column = table["columns"]["PDCSAP_FLUX"]
    row_count = int(table["row_count"])

    windows = []
    with Path(fits_path).open("rb") as handle:
        time_values = [None] * (row_count + 1)
        flux_values = [None] * (row_count + 1)

        for row_number in range(1, row_count + 1):
            time_value = read_value(handle, table, time_column, row_number)
            flux_value = read_value(handle, table, flux_column, row_number)
            if math.isfinite(time_value) and math.isfinite(flux_value):
                time_values[row_number] = time_value
                flux_values[row_number] = flux_value

        for start_row in range(1, row_count - WINDOW_LENGTH + 2):
            end_row = start_row + WINDOW_LENGTH - 1
            segment_flux = []
            finite = True

            for row_number in range(start_row, end_row + 1):
                if time_values[row_number] is None or flux_values[row_number] is None:
                    finite = False
                    break
                segment_flux.append(flux_values[row_number])

            if not finite:
                continue

            mean_flux, mean_abs_residual = constant_flux_mean_abs_residual(segment_flux)
            windows.append(
                {
                    "start_row": start_row,
                    "end_row": end_row,
                    "mean_flux": mean_flux,
                    "mean_abs_residual": mean_abs_residual,
                }
            )

    return windows, row_count


def expected_receipts(receipt_path, multisegment_path, family_path, windows, row_count):
    residuals = [window["mean_abs_residual"] for window in windows]
    min_index = min(range(len(windows)), key=lambda i: residuals[i])
    max_index = max(range(len(windows)), key=lambda i: residuals[i])
    median_residual = statistics.median(residuals)

    non_claims = [
        "gravity closure",
        "cosmology closure",
        "Chronos-RR closure",
        "physical time theorem closure",
        "ZeroDay closure",
    ]

    family = {
        "receipt_name": "KeplerAllWindowSegmentFamilySummaryReceipt",
        "receipt_class": "ALL_WINDOW_SEGMENT_FAMILY_SUMMARY",
        "source_receipt": str(receipt_path),
        "source_multisegment_receipt": str(multisegment_path),
        "window_length_rows": WINDOW_LENGTH,
        "segment_selection_rule": SELECTION_RULE,
        "time_column": "TIME",
        "flux_column": "PDCSAP_FLUX",
        "row_count": row_count,
        "finite_window_count": len(windows),
        "summary_statistics": {
            "min_mean_abs_residual": residuals[min_index],
            "median_mean_abs_residual": median_residual,
            "max_mean_abs_residual": residuals[max_index],
            "min_residual_window": {
                "start_row": windows[min_index]["start_row"],
                "end_row": windows[min_index]["end_row"],
            },
            "max_residual_window": {
                "start_row": windows[max_index]["start_row"],
                "end_row": windows[max_index]["end_row"],
            },
        },
        "allowed_output": ALLOWED_OUTPUT,
        "non_claims": non_claims,
    }

    selection_bias = {
        "receipt_name": "KeplerAllWindowAntiSelectionBiasReceipt",
        "receipt_class": "ANTI_SELECTION_BIAS_BOUNDARY",
        "source_family_receipt": str(family_path),
        "allowed_selection_rule": SELECTION_RULE,
        "forbidden_selection_rules": [
            "select windows by minimizing residual before reporting family statistics",
            "select windows by maximizing signal before reporting family statistics",
            "select windows using Chronos-RR target",
            "select windows using gravity target",
            "select windows using cosmology target",
            "select windows using ZeroDay target",
            "discard finite windows after inspecting comparator values",
        ],
        "required_statistics": [
            "finite_window_count",
            "min_mean_abs_residual",
            "median_mean_abs_residual",
            "max_mean_abs_residual",
        ],
        "model_boundary": [
            "constant-flux null comparator only",
            "all-window finite scan only",
            "no astrophysical model fitting",
            "no hidden detrending",
            "no closure inference",
            "no theorem promotion",
        ],
        "non_claims": non_claims,
    }

    return family, selection_bias


def verify(receipt_path, multisegment_path, family_path, selection_bias_path, mode):
    receipt_path = Path(receipt_path)
    multisegment_path = Path(multisegment_path)
    family_path = Path(family_path)
    selection_bias_path = Path(selection_bias_path)

    receipt = load_json(receipt_path)
    multisegment = load_json(multisegment_path)

    if receipt.get("receipt_class") != "PINNED_MAST_FITS_EVIDENCE":
        fail("All-window scan requires PINNED_MAST_FITS_EVIDENCE.")
    if receipt.get("time_column") != "TIME":
        fail("All-window verifier is bound to TIME.")
    if receipt.get("flux_column") != "PDCSAP_FLUX":
        fail("All-window verifier is bound to PDCSAP_FLUX.")

    fits_path = receipt_path.parent / receipt.get("filename", "")
    if not fits_path.exists():
        fail(f"MISSING_OBJECT := {fits_path}")

    module = load_semantic_module()
    actual_hash = module.sha256_file(fits_path)
    if actual_hash != receipt.get("sha256"):
        fail(f"FITS SHA-256 mismatch. Expected {receipt.get('sha256')}, got {actual_hash}")

    table = module.find_binary_table_with_columns(fits_path, {"TIME", "PDCSAP_FLUX"})
    windows, row_count = scan_windows(fits_path, table)
    if not windows:
        fail("MISSING_OBJECT := at least one finite 100-row TIME/PDCSAP_FLUX window")

    expected_family, expected_selection_bias = expected_receipts(
        receipt_path,
        multisegment_path,
        family_path,
        windows,
        row_count,
    )

    if mode == "--write":
        write_json(family_path, expected_family)
        write_json(selection_bias_path, expected_selection_bias)

    family = load_json(family_path)
    selection_bias = load_json(selection_bias_path)
    boundary_check(receipt, multisegment, family, selection_bias)

    if family != expected_family:
        fail("All-window segment-family summary receipt does not match deterministic verifier output.")
    if selection_bias != expected_selection_bias:
        fail("Anti-selection-bias receipt does not match deterministic verifier output.")

    stats = family["summary_statistics"]
    print("KEPLER_ALL_WINDOW_SEGMENT_FAMILY_OK")
    print(f"WINDOW_LENGTH_ROWS := {WINDOW_LENGTH}")
    print(f"ROW_COUNT := {family['row_count']}")
    print(f"FINITE_WINDOW_COUNT := {family['finite_window_count']}")
    print(f"MIN_MEAN_ABS_RESIDUAL := {stats['min_mean_abs_residual']:.12g}")
    print(f"MEDIAN_MEAN_ABS_RESIDUAL := {stats['median_mean_abs_residual']:.12g}")
    print(f"MAX_MEAN_ABS_RESIDUAL := {stats['max_mean_abs_residual']:.12g}")
    print(f"MIN_RESIDUAL_WINDOW := {stats['min_residual_window']['start_row']}..{stats['min_residual_window']['end_row']}")
    print(f"MAX_RESIDUAL_WINDOW := {stats['max_residual_window']['start_row']}..{stats['max_residual_window']['end_row']}")
    print("BOUNDARY := no gravity/cosmology/Chronos-RR/physical-time/ZeroDay closure")


if __name__ == "__main__":
    if len(sys.argv) not in {5, 6}:
        fail(
            "Usage: verify_kepler_all_window_segment_family.py "
            "<receipt.json> <multisegment.json> <family.json> <anti_selection_bias.json> [--write]"
        )
    mode = sys.argv[5] if len(sys.argv) == 6 else "--verify"
    if mode not in {"--write", "--verify"}:
        fail("mode must be --write or --verify")
    verify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], mode)
