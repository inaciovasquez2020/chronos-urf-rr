#!/usr/bin/env python3
from __future__ import annotations

import json
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path
from typing import Any

getcontext().prec = 80

ARTIFACT_PATH = Path(
    "artifacts/external_validation/"
    "jet_laplacian_interval_operator_boundary_2026_06_29.json"
)

FORBIDDEN_CLAIM_FRAGMENTS = (
    "proves Jet-Laplacian rank stability",
    "proves jet-laplacian rank stability",
    "proves spectral stability",
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


def require_interval(entry: Any, label: str) -> tuple[Decimal, Decimal]:
    if not isinstance(entry, dict):
        raise SystemExit(f"INVALID_INTERVAL := {label}")
    if "lo" not in entry or "hi" not in entry:
        raise SystemExit(f"MISSING_INTERVAL_ENDPOINT := {label}")
    lo = decimal_value(entry["lo"], f"{label}.lo")
    hi = decimal_value(entry["hi"], f"{label}.hi")
    if lo > hi:
        raise SystemExit(f"INVALID_INTERVAL_ORDER := {label}")
    return lo, hi


def main() -> None:
    if not ARTIFACT_PATH.exists():
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT_PATH}")

    text = ARTIFACT_PATH.read_text(encoding="utf-8")
    data = json.loads(text)

    if data.get("status") != "interval_operator_certificate_boundary_only":
        raise SystemExit("INVALID_STATUS := expected interval_operator_certificate_boundary_only")

    operator = data.get("operator")
    if not isinstance(operator, dict):
        raise SystemExit("MISSING_OBJECT := operator")

    dimension = operator.get("dimension")
    if not isinstance(dimension, int) or dimension <= 0:
        raise SystemExit("INVALID_DIMENSION := operator.dimension")

    rows = operator.get("interval_matrix_rows")
    if not isinstance(rows, list) or len(rows) != dimension:
        raise SystemExit("INVALID_MATRIX_ROW_COUNT := operator.interval_matrix_rows")

    for i, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != dimension:
            raise SystemExit(f"INVALID_MATRIX_COLUMN_COUNT := row {i}")
        for j, entry in enumerate(row):
            require_interval(entry, f"operator.interval_matrix_rows[{i}][{j}]")

    inverse_payload = data.get("certified_inverse_or_pseudoinverse_bound")
    if not isinstance(inverse_payload, dict):
        raise SystemExit("MISSING_OBJECT := certified_inverse_or_pseudoinverse_bound")
    inverse_bound = decimal_value(inverse_payload.get("bound"), "certified_inverse_or_pseudoinverse_bound.bound")
    if inverse_bound < 0:
        raise SystemExit("INVALID_BOUND := certified_inverse_or_pseudoinverse_bound.bound must be nonnegative")
    if inverse_payload.get("field_is_certificate_bound_only") is not True:
        raise SystemExit("INVALID_BOUNDARY_FLAG := certified_inverse_or_pseudoinverse_bound")

    distance_payload = data.get("distance_axis_lipschitz_bound")
    if not isinstance(distance_payload, dict):
        raise SystemExit("MISSING_OBJECT := distance_axis_lipschitz_bound")
    distance_bound = decimal_value(distance_payload.get("bound"), "distance_axis_lipschitz_bound.bound")
    if distance_bound < 0:
        raise SystemExit("INVALID_BOUND := distance_axis_lipschitz_bound.bound must be nonnegative")
    if distance_payload.get("field_is_certificate_bound_only") is not True:
        raise SystemExit("INVALID_BOUNDARY_FLAG := distance_axis_lipschitz_bound")

    for fragment in FORBIDDEN_CLAIM_FRAGMENTS:
        if fragment in text:
            raise SystemExit(f"FORBIDDEN_CLAIM_FRAGMENT := {fragment}")

    nonclaims = data.get("nonclaims")
    if not isinstance(nonclaims, list) or not nonclaims:
        raise SystemExit("MISSING_OBJECT := nonclaims")

    print("JET_LAPLACIAN_DISTANCE_AXIS_LIPSCHITZ_BOUNDARY_OK")


if __name__ == "__main__":
    main()
