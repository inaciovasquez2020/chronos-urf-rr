#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/RotationCurveResidualDeficitMassBridge.lean"
ART = ROOT / "artifacts/chronos/rotation_curve_residual_deficit_mass_bridge_2026_05_28.json"
DOC = ROOT / "docs/status/ROTATION_CURVE_RESIDUAL_DEFICIT_MASS_BRIDGE_2026_05_28.md"

REQUIRED_TOKENS = [
    "RotationCurveResidualDeficitMassBridge",
    "ROTATION_CURVE_RESIDUAL_DEFICIT_MASS_BRIDGE_2026_05_28",
    "FINITE_DEFICIT_MASS_ACCOUNTING_BRIDGE_ONLY",
    "no empirical rotation-curve fit",
    "no galaxy data ingestion",
    "no dark matter replacement",
    "no Lambda-CDM failure",
    "no modified gravity claim",
    "no empirical detector correctness",
    "no Einstein-matter PDE well-posedness",
    "no trapped-surface formation",
    "no black-hole formation",
    "no cosmic censorship",
    "no hoop conjecture",
    "no unrestricted QL_CollapseGate",
    "no unrestricted UniversalBoundaryCompactness",
    "no unrestricted Chronos-RR",
    "no unrestricted H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]


def require_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return path.read_text()


def main() -> None:
    lean_text = require_file(LEAN)
    doc_text = require_file(DOC)
    artifact = json.loads(require_file(ART))

    combined = "\n".join([lean_text, doc_text, json.dumps(artifact, sort_keys=True)])

    missing = [token for token in REQUIRED_TOKENS if token not in combined]
    if missing:
        raise SystemExit(f"missing required tokens: {missing}")

    if artifact.get("status") != "FINITE_DEFICIT_MASS_ACCOUNTING_BRIDGE_ONLY":
        raise SystemExit("artifact status mismatch")

    if artifact.get("object") != "RotationCurveResidualDeficitMassBridge":
        raise SystemExit("artifact object mismatch")

    print("ROTATION_CURVE_RESIDUAL_DEFICIT_MASS_BRIDGE_OK")


if __name__ == "__main__":
    main()
