#!/usr/bin/env python3
from __future__ import annotations

import json
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path
from typing import Any

getcontext().prec = 80

ARTIFACT_PATH = Path(
    "artifacts/external_validation/"
    "jet_laplacian_rank_margin_payload_2026_06_29.json"
)
NK_PATH = Path(
    "artifacts/external_validation/"
    "jet_laplacian_newton_kantorovich_boundary_2026_06_29.json"
)

FORBIDDEN_CLAIM_FRAGMENTS = (
    "proves Jet-Laplacian rank stability",
    "proves jet-laplacian rank stability",
    "proves spectral stability",
    "proves a global rank theorem",
    "proves gravity",
    "proves Einstein",
    "proves metric-backreaction",
    "proves continuum",
    "proves Navier-Stokes",
    "proves blow-up",
)


def decimal_value(value: Any, label: str) -> Decimal:
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise SystemExit(f"INVALID_DECIMAL := {label}") from exc
    if not number.is_finite():
        raise SystemExit(f"NONFINITE_DECIMAL := {label}")
    return number


def main() -> None:
    if not ARTIFACT_PATH.exists():
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT_PATH}")
    if not NK_PATH.exists():
        raise SystemExit(f"MISSING_OBJECT := {NK_PATH}")

    text = ARTIFACT_PATH.read_text(encoding="utf-8")
    data = json.loads(text)
    nk = json.loads(NK_PATH.read_text(encoding="utf-8"))

    if data.get("status") != "rank_margin_certificate_boundary_only":
        raise SystemExit("INVALID_STATUS := expected rank_margin_certificate_boundary_only")

    witness = data.get("witness")
    if not isinstance(witness, dict):
        raise SystemExit("MISSING_OBJECT := witness")
    if witness.get("shape") != [36, 36]:
        raise SystemExit("INVALID_SHAPE := witness.shape")
    for field, expected in {
        "num_nodes": 4,
        "dimension": 3,
        "jet_order": 2,
        "projection_rank": 2,
        "seed": 20260628,
    }.items():
        if witness.get(field) != expected:
            raise SystemExit(f"INVALID_WITNESS_FIELD := {field}")

    interval_matrix = data.get("interval_matrix")
    if not isinstance(interval_matrix, dict):
        raise SystemExit("MISSING_OBJECT := interval_matrix")
    radius = decimal_value(interval_matrix.get("radius"), "interval_matrix.radius")
    if radius <= 0:
        raise SystemExit("INVALID_RADIUS := interval_matrix.radius")

    rows = interval_matrix.get("rows")
    if not isinstance(rows, list) or len(rows) != 36:
        raise SystemExit("INVALID_ROW_COUNT := interval_matrix.rows")
    for i, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 36:
            raise SystemExit(f"INVALID_COLUMN_COUNT := row {i}")
        for j, entry in enumerate(row):
            if not isinstance(entry, dict):
                raise SystemExit(f"INVALID_INTERVAL_ENTRY := [{i}][{j}]")
            lo = decimal_value(entry.get("lo"), f"rows[{i}][{j}].lo")
            hi = decimal_value(entry.get("hi"), f"rows[{i}][{j}].hi")
            if lo > hi:
                raise SystemExit(f"INVALID_INTERVAL_ORDER := [{i}][{j}]")

    cert = data.get("rank_margin_certificate")
    if not isinstance(cert, dict):
        raise SystemExit("MISSING_OBJECT := rank_margin_certificate")
    if cert.get("numeric_rank") != 35:
        raise SystemExit("INVALID_NUMERIC_RANK := expected 35")
    if cert.get("structural_nullity") != 1:
        raise SystemExit("INVALID_STRUCTURAL_NULLITY := expected 1")
    if cert.get("certificate_bound_only") is not True:
        raise SystemExit("INVALID_BOUNDARY_FLAG := rank_margin_certificate")

    smallest_positive = decimal_value(
        cert.get("smallest_positive_singular_value"),
        "rank_margin_certificate.smallest_positive_singular_value",
    )
    frob_error = decimal_value(
        cert.get("frobenius_interval_error_bound"),
        "rank_margin_certificate.frobenius_interval_error_bound",
    )
    lower = decimal_value(
        cert.get("rank_margin_lower_bound"),
        "rank_margin_certificate.rank_margin_lower_bound",
    )
    if smallest_positive <= 0:
        raise SystemExit("INVALID_MARGIN := smallest_positive_singular_value must be positive")
    if frob_error < 0:
        raise SystemExit("INVALID_MARGIN := frobenius_interval_error_bound must be nonnegative")
    if lower != smallest_positive - frob_error:
        raise SystemExit("INVALID_MARGIN := rank_margin_lower_bound mismatch")
    if lower <= 0:
        raise SystemExit("INVALID_MARGIN := rank_margin_lower_bound must be positive")

    connection = data.get("contraction_margin_connection")
    if not isinstance(connection, dict):
        raise SystemExit("MISSING_OBJECT := contraction_margin_connection")
    if connection.get("field") != "contraction_margin":
        raise SystemExit("INVALID_CONNECTION_FIELD := contraction_margin")
    if connection.get("connection_is_certificate_only") is not True:
        raise SystemExit("INVALID_CONNECTION_BOUNDARY_FLAG")

    contraction_margin = decimal_value(nk.get("contraction_margin"), "newton_kantorovich.contraction_margin")
    if contraction_margin <= 0:
        raise SystemExit("INVALID_CONTRACTION_MARGIN := expected positive")

    for fragment in FORBIDDEN_CLAIM_FRAGMENTS:
        if fragment in text:
            raise SystemExit(f"FORBIDDEN_CLAIM_FRAGMENT := {fragment}")

    nonclaims = data.get("nonclaims")
    if not isinstance(nonclaims, list) or not nonclaims:
        raise SystemExit("MISSING_OBJECT := nonclaims")

    print("JET_LAPLACIAN_RANK_MARGIN_PAYLOAD_OK")


if __name__ == "__main__":
    main()
