#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path
from typing import Any

getcontext().prec = 80

BRIDGE_PATH = Path(
    "artifacts/external_validation/"
    "rank_margin_to_stability_bridge_boundary_2026_06_29.json"
)
RANK_MARGIN_PATH = Path(
    "artifacts/external_validation/"
    "jet_laplacian_rank_margin_payload_2026_06_29.json"
)

FORBIDDEN_CLAIM_FRAGMENTS = (
    "proves Jet-Laplacian rank stability",
    "proves jet-laplacian rank stability",
    "proves threshold crossing",
    "proves restricted concentration",
    "proves analytic Einstein",
    "proves Einstein-matter",
    "proves gravity closure",
    "proves global rank stability",
)

REQUIRED_NONCLAIMS = {
    "no_unconditional_restricted_concentration_monotonicity_theorem",
    "no_threshold_crossing_proof",
    "no_gravity_closure",
    "no_analytic_einstein_matter_bootstrap",
    "no_global_rank_stability_theorem",
}


def decimal_value(value: Any, label: str) -> Decimal:
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise SystemExit(f"INVALID_DECIMAL := {label}") from exc
    if not number.is_finite():
        raise SystemExit(f"NONFINITE_DECIMAL := {label}")
    return number


def main() -> None:
    if not BRIDGE_PATH.exists():
        raise SystemExit(f"MISSING_OBJECT := {BRIDGE_PATH}")
    if not RANK_MARGIN_PATH.exists():
        raise SystemExit(f"MISSING_OBJECT := {RANK_MARGIN_PATH}")

    bridge_text = BRIDGE_PATH.read_text(encoding="utf-8")
    bridge = json.loads(bridge_text)
    rank_payload = json.loads(RANK_MARGIN_PATH.read_text(encoding="utf-8"))

    if bridge.get("status") != "conditional_frontier_surface_only":
        raise SystemExit("INVALID_STATUS := expected conditional_frontier_surface_only")

    bridge_block = bridge.get("bridge")
    if not isinstance(bridge_block, dict):
        raise SystemExit("MISSING_OBJECT := bridge")

    if bridge_block.get("source_field") != "rank_margin_certificate.rank_margin_lower_bound":
        raise SystemExit("INVALID_SOURCE_FIELD := rank_margin_certificate.rank_margin_lower_bound")
    if bridge_block.get("target_field") != "conditional_stability_coefficient":
        raise SystemExit("INVALID_TARGET_FIELD := conditional_stability_coefficient")
    if bridge_block.get("terminal_assumption") != "FGL_k_R_B":
        raise SystemExit("INVALID_TERMINAL_ASSUMPTION := FGL_k_R_B")
    if bridge_block.get("status_lock") != "BUILD_CLOSEOUT_SURFACE_ONLY_NO_ANALYTIC_PACKAGE_PROOF":
        raise SystemExit("INVALID_STATUS_LOCK")
    if bridge_block.get("connection_is_diagnostic_only") is not True:
        raise SystemExit("INVALID_BOUNDARY_FLAG := connection_is_diagnostic_only")

    required_nonclaims = bridge.get("required_nonclaims")
    if not isinstance(required_nonclaims, list):
        raise SystemExit("MISSING_OBJECT := required_nonclaims")
    if set(required_nonclaims) != REQUIRED_NONCLAIMS:
        raise SystemExit("INVALID_REQUIRED_NONCLAIMS")

    cert = rank_payload.get("rank_margin_certificate")
    if not isinstance(cert, dict):
        raise SystemExit("MISSING_OBJECT := rank_margin_certificate")
    margin = decimal_value(cert.get("rank_margin_lower_bound"), "rank_margin_certificate.rank_margin_lower_bound")
    if margin <= 0:
        raise SystemExit("INVALID_MARGIN := rank_margin_lower_bound must be positive")

    coefficient = 1.0 / (1.0 + math.exp(-float(margin)))
    if not (0.5 < coefficient < 1.0):
        raise SystemExit("INVALID_COEFFICIENT_RANGE := expected 0.5 < coefficient < 1")

    for fragment in FORBIDDEN_CLAIM_FRAGMENTS:
        if fragment in bridge_text:
            raise SystemExit(f"FORBIDDEN_CLAIM_FRAGMENT := {fragment}")

    nonclaims = bridge.get("nonclaims")
    if not isinstance(nonclaims, list) or not nonclaims:
        raise SystemExit("MISSING_OBJECT := nonclaims")

    print("RANK_MARGIN_TO_STABILITY_BRIDGE_BOUNDARY_OK")
    print(f"CONDITIONAL_STABILITY_COEFFICIENT := {coefficient:.17g}")


if __name__ == "__main__":
    main()
