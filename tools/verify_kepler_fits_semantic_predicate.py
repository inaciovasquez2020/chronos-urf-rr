#!/usr/bin/env python3
import hashlib
import json
import math
import re
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

ALLOWED_OUTPUT = "FINITE_LIGHT_CURVE_SEGMENT_COMPARED_TO_CONSTANT_NULL"


def fail(message):
    print(f"ERROR: {message}")
    raise SystemExit(1)


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fits_blocks(handle):
    while True:
        header_bytes = bytearray()
        while True:
            block = handle.read(2880)
            if not block:
                return
            if len(block) != 2880:
                fail("Truncated FITS header block.")
            header_bytes.extend(block)
            cards = [
                bytes(header_bytes[i:i + 80]).decode("ascii", errors="replace")
                for i in range(0, len(header_bytes), 80)
            ]
            if any(card.startswith("END") for card in cards):
                break

        header = parse_header(cards)
        data_size = hdu_data_size(header)
        data_start = handle.tell()
        yield header, data_start, data_size
        padded_size = ((data_size + 2879) // 2880) * 2880
        handle.seek(data_start + padded_size)


def parse_header(cards):
    header = {}
    ordered_cards = []
    for card in cards:
        key = card[:8].strip()
        ordered_cards.append(card)
        if not key or key == "END":
            continue
        if len(card) > 8 and card[8] == "=":
            raw_value = card[10:80].split("/", 1)[0].strip()
            header[key] = parse_value(raw_value)
    header["_cards"] = ordered_cards
    return header


def parse_value(raw):
    if raw.startswith("'"):
        end = raw.find("'", 1)
        if end >= 0:
            return raw[1:end].strip()
        return raw.strip("'").strip()
    if raw in {"T", "F"}:
        return raw == "T"
    try:
        if any(c in raw for c in ".EeDd"):
            return float(raw.replace("D", "E"))
        return int(raw)
    except ValueError:
        return raw


def hdu_data_size(header):
    naxis = int(header.get("NAXIS", 0) or 0)
    if naxis == 0:
        return 0
    bitpix = int(header.get("BITPIX", 8))
    if header.get("XTENSION") == "BINTABLE":
        row_len = int(header.get("NAXIS1", 0))
        row_count = int(header.get("NAXIS2", 0))
        pcount = int(header.get("PCOUNT", 0))
        return row_len * row_count + pcount

    size = abs(bitpix) // 8
    for axis in range(1, naxis + 1):
        size *= int(header.get(f"NAXIS{axis}", 0))
    size += int(header.get("PCOUNT", 0) or 0)
    return size


def parse_tform(tform):
    match = re.fullmatch(r"(\d*)([A-Z])", str(tform).strip())
    if not match:
        fail(f"Unsupported FITS TFORM: {tform}")
    repeat = int(match.group(1) or "1")
    code = match.group(2)
    sizes = {
        "L": 1,
        "X": 1,
        "B": 1,
        "I": 2,
        "J": 4,
        "K": 8,
        "A": 1,
        "E": 4,
        "D": 8,
    }
    if code not in sizes:
        fail(f"Unsupported FITS column format code: {code}")
    return repeat, code, repeat * sizes[code]


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


def find_binary_table_with_columns(fits_path, required_columns):
    with fits_path.open("rb") as handle:
        for header, data_start, data_size in fits_blocks(handle):
            if header.get("XTENSION") != "BINTABLE":
                continue

            tfields = int(header.get("TFIELDS", 0))
            row_len = int(header.get("NAXIS1", 0))
            row_count = int(header.get("NAXIS2", 0))

            offset = 0
            columns = {}
            for index in range(1, tfields + 1):
                name = str(header.get(f"TTYPE{index}", "")).strip()
                tform = header.get(f"TFORM{index}")
                repeat, code, size = parse_tform(tform)
                columns[name] = {
                    "index": index,
                    "offset": offset,
                    "repeat": repeat,
                    "code": code,
                    "size": size,
                    "tform": tform,
                }
                offset += size

            if offset > row_len:
                fail("Parsed FITS table columns exceed NAXIS1 row length.")

            if required_columns.issubset(columns):
                return {
                    "header": header,
                    "data_start": data_start,
                    "data_size": data_size,
                    "row_len": row_len,
                    "row_count": row_count,
                    "columns": columns,
                }

    fail(f"No FITS binary table contains required columns: {sorted(required_columns)}")


def extract_column_interval(fits_path, table, column_name, start_row, end_row):
    if start_row < 1:
        fail("finite_interval.start_row must be >= 1.")
    if end_row < start_row:
        fail("finite_interval.end_row must be >= start_row.")
    if end_row > table["row_count"]:
        fail(f"finite interval ends at row {end_row}, but table has only {table['row_count']} rows.")

    column = table["columns"][column_name]
    if column["repeat"] != 1:
        fail(f"Column {column_name} must be scalar; got repeat={column['repeat']}.")

    values = []
    with fits_path.open("rb") as handle:
        for row_number in range(start_row, end_row + 1):
            row_offset = table["data_start"] + (row_number - 1) * table["row_len"]
            handle.seek(row_offset + column["offset"])
            raw = handle.read(column["size"])
            if len(raw) != column["size"]:
                fail(f"Could not read complete value for {column_name} at row {row_number}.")
            value = read_scalar(raw, column["code"])
            if not math.isfinite(value):
                fail(f"Non-finite {column_name} value at row {row_number}.")
            values.append(value)
    return values


def verify(receipt_path, predicate_path):
    receipt_path = Path(receipt_path)
    predicate_path = Path(predicate_path)

    receipt = json.loads(receipt_path.read_text())
    predicate = json.loads(predicate_path.read_text())

    raw_text = json.dumps({"receipt": receipt, "predicate": predicate}, sort_keys=True)
    for term in FORBIDDEN_PROMOTIONS:
        if term in raw_text:
            fail(f"Anti-promotion guard triggered. Forbidden term '{term}' identified.")

    non_claims = set(receipt.get("non_claims", [])) | set(predicate.get("non_claims", []))
    if not REQUIRED_NON_CLAIMS.issubset(non_claims):
        fail("Missing mandatory boundary non-claims.")

    if receipt.get("receipt_class") != "PINNED_MAST_FITS_EVIDENCE":
        fail("FITS semantic predicate requires receipt_class=PINNED_MAST_FITS_EVIDENCE.")

    if receipt.get("null_comparator_output") != ALLOWED_OUTPUT:
        fail("Receipt null_comparator_output does not match allowed output.")

    fits_path = receipt_path.parent / receipt.get("filename", "")
    if not fits_path.exists():
        fail(f"Missing local FITS artifact: {fits_path}")

    actual_hash = sha256_file(fits_path)
    if actual_hash != receipt.get("sha256"):
        fail(f"FITS SHA-256 mismatch. Expected {receipt.get('sha256')}, got {actual_hash}")

    flux_column = receipt.get("flux_column")
    time_column = receipt.get("time_column")
    if flux_column != "PDCSAP_FLUX":
        fail("This verifier currently binds the null comparator to PDCSAP_FLUX.")
    if time_column != "TIME":
        fail("This verifier currently binds the time coordinate to TIME.")

    interval = receipt.get("finite_interval", {})
    start_row = int(interval.get("start_row"))
    end_row = int(interval.get("end_row"))

    table = find_binary_table_with_columns(fits_path, {time_column, flux_column})
    time_values = extract_column_interval(fits_path, table, time_column, start_row, end_row)
    flux_values = extract_column_interval(fits_path, table, flux_column, start_row, end_row)

    mean_flux = sum(flux_values) / len(flux_values)
    mean_abs_residual = sum(abs(value - mean_flux) for value in flux_values) / len(flux_values)

    if not math.isfinite(mean_flux) or not math.isfinite(mean_abs_residual):
        fail("Null comparator produced non-finite statistic.")

    print("KEPLER_FITS_SEMANTIC_PREDICATE_OK")
    print(f"ROWS_VERIFIED := {start_row}..{end_row}")
    print(f"TIME_COLUMN := {time_column}")
    print(f"FLUX_COLUMN := {flux_column}")
    print(f"NULL_COMPARATOR := constant_flux_mean_residual")
    print(f"MEAN_FLUX := {mean_flux:.12g}")
    print(f"MEAN_ABS_RESIDUAL := {mean_abs_residual:.12g}")
    print("BOUNDARY := no gravity/cosmology/Chronos-RR/physical-time/ZeroDay closure")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        fail("Usage: verify_kepler_fits_semantic_predicate.py <receipt.json> <predicate.json>")
    verify(sys.argv[1], sys.argv[2])
