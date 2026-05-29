#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ROOT / "lean/Chronos/Frontier/ConcreteRotationCurvePredictionVectorSchema.lean",
    ROOT / "lean/Chronos/Frontier/RotationCurveGalaxyDataIngestionAdapter.lean",
    ROOT / "lean/Chronos/Frontier/RotationCurveLikelihoodModelComparisonExecutionGate.lean",
    ROOT / "docs/status/ROTATION_CURVE_PREDICTION_COMPARISON_EXECUTION_CHAIN_2026_05_28.md",
]

ART = ROOT / "artifacts/chronos/rotation_curve_prediction_comparison_execution_chain_2026_05_28.json"

REQUIRED_TOKENS = [
    "ROTATION_CURVE_PREDICTION_COMPARISON_EXECUTION_CHAIN_2026_05_28",
    "INTERFACE_CHAIN_ONLY_EMPIRICAL_RUN_OPEN",
    "ConcreteRotationCurvePredictionVectorSchema",
    "RotationCurveGalaxyDataIngestionAdapter",
    "RotationCurveLikelihoodModelComparisonExecutionGate",
    "ActualGalaxyRotationCurveEmpiricalRun",
    "AuthenticGalaxyRotationCurvePayload",
    "BaselineModelPredictionVector",
    "DeficitMassModelPredictionVector",
    "LikelihoodComparisonResult",
    "no empirical rotation-curve fit",
    "no galaxy data ingestion",
    "no authentic galaxy data bound",
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

    if artifact.get("status") != "INTERFACE_CHAIN_ONLY_EMPIRICAL_RUN_OPEN":
        raise SystemExit("artifact status mismatch")

    if len(artifact.get("objects_added", [])) != 3:
        raise SystemExit("expected exactly three interface objects")

    print("ROTATION_CURVE_PREDICTION_COMPARISON_EXECUTION_CHAIN_OK")


if __name__ == "__main__":
    main()
