#!/usr/bin/env python3
from __future__ import annotations

import json
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path
from typing import Any

getcontext().prec = 80

ARTIFACT_PATH = Path(
    "artifacts/external_validation/"
    "jet_laplacian_newton_kantorovich_boundary_2026_06_29.json"
)

REQUIRED_FIELDS = (
    "residual_bound_Z0",
    "linearization_defect_Z1",
    "lipschitz_bound_K",
    "radius_r",
    "contraction_margin",
)

FORBIDDEN_CLAIM_FRAGMENTS = (
    "proves Jet-Laplacian rank stability",
    "proves jet-laplacian rank stability",
    "proves spectral stability",
    "proves gravity",
    "proves continuum",
    "proves Navier-Stokes",
    "proves blow-up",
)


def decimal_field(data: dict[str, Any], field: str) -> Decimal:
    if field not in data:
        raise SystemExit(f"MISSING_FIELD := {field}")
    value = data[field]
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise SystemExit(f"INVALID_DECIMAL_FIELD := {field}") from exc
    if not number.is_finite():
        raise SystemExit(f"NONFINITE_DECIMAL_FIELD := {field}")
    return number


def main() -> None:
    if not ARTIFACT_PATH.exists():
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT_PATH}")

    data = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))

    for field in REQUIRED_FIELDS:
        if field not in data:
            raise SystemExit(f"MISSING_FIELD := {field}")

    z0 = decimal_field(data, "residual_bound_Z0")
    z1 = decimal_field(data, "linearization_defect_Z1")
    k = decimal_field(data, "lipschitz_bound_K")
    r = decimal_field(data, "radius_r")
    stated_margin = decimal_field(data, "contraction_margin")

    if z0 < 0:
        raise SystemExit("INVALID_BOUND := residual_bound_Z0 must be nonnegative")
    if not (Decimal("0") <= z1 < Decimal("1")):
        raise SystemExit("INVALID_BOUND := expected 0 <= linearization_defect_Z1 < 1")
    if k < 0:
        raise SystemExit("INVALID_BOUND := lipschitz_bound_K must be nonnegative")
    if r <= 0:
        raise SystemExit("INVALID_BOUND := radius_r must be positive")

    contraction_left = Decimal("2") * k * z0
    contraction_right = (Decimal("1") - z1) ** 2
    computed_margin = contraction_right - contraction_left

    if contraction_left > contraction_right:
        raise SystemExit("CONTRACTION_CONDITION_FAILED := 2*K*Z0 <= (1 - Z1)^2")

    if stated_margin != computed_margin:
        raise SystemExit(
            "INVALID_MARGIN := contraction_margin must equal "
            "(1 - Z1)^2 - 2*K*Z0"
        )

    artifact_text = ARTIFACT_PATH.read_text(encoding="utf-8")
    for fragment in FORBIDDEN_CLAIM_FRAGMENTS:
        if fragment in artifact_text:
            raise SystemExit(f"FORBIDDEN_CLAIM_FRAGMENT := {fragment}")

    if data.get("status") != "boundary_certificate_only":
        raise SystemExit("INVALID_STATUS := expected boundary_certificate_only")

    print("JET_LAPLACIAN_NEWTON_KANTOROVICH_BOUNDARY_OK")


if __name__ == "__main__":
    main()
