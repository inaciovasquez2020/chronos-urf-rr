#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ROOT / "lean/Chronos/Frontier/BoundedSyntheticRotationCurvePayloadGate.lean",
    ROOT / "lean/Chronos/Frontier/AuthenticSPARCRotationCurvePayloadBinding.lean",
    ROOT / "docs/status/ROTATION_CURVE_PAYLOAD_GATES_2026_05_28.md",
]

ART = ROOT / "artifacts/chronos/rotation_curve_payload_gates_2026_05_28.json"

REQUIRED_TOKENS = [
    "ROTATION_CURVE_PAYLOAD_GATES_2026_05_28",
    "PAYLOAD_GATES_ONLY_NO_AUTHENTIC_DATA_BOUND",
    "BoundedSyntheticRotationCurvePayloadGate",
    "AuthenticSPARCRotationCurvePayloadBinding",
    "RotationCurveAuthenticPayloadTarget",
    "SPARC Galaxy Rotation Curve",
    "10.5281/zenodo.16284118",
    "https://zenodo.org/records/16284118",
    "AuthenticSPARCPayloadDownload",
    "SPARCPayloadDigestVerification",
    "SPARCSchemaValidationRun",
    "BaselineModelPredictionVector",
    "DeficitMassModelPredictionVector",
    "LikelihoodComparisonResult",
    "ActualGalaxyRotationCurveEmpiricalRun",
    "no SPARC payload downloaded",
    "no payload digest verified",
    "no SPARC schema validation run",
    "no authentic galaxy data bound",
    "no empirical rotation-curve fit",
    "no galaxy data ingestion",
    "no actual empirical run",
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
    artifact = json.loads(require_file(ART))
    combined = json.dumps(artifact, sort_keys=True) + "\n" + "\n".join(
        require_file(path) for path in FILES
    )

    missing = [token for token in REQUIRED_TOKENS if token not in combined]
    if missing:
        raise SystemExit(f"missing required tokens: {missing}")

    if artifact.get("status") != "PAYLOAD_GATES_ONLY_NO_AUTHENTIC_DATA_BOUND":
        raise SystemExit("artifact status mismatch")

    if len(artifact.get("objects_added", [])) != 2:
        raise SystemExit("expected exactly two payload-gate objects")

    print("ROTATION_CURVE_PAYLOAD_GATES_OK")


if __name__ == "__main__":
    main()
