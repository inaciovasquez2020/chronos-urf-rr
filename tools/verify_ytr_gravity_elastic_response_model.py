#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ART = ROOT / "artifacts/chronos/ytr_gravity_elastic_response_model_2026_05_29.json"
DOC = ROOT / "docs/status/YTR_GRAVITY_ELASTIC_RESPONSE_MODEL_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/YtRGravityElasticResponseModel.lean"
CHRONOS = ROOT / "lean/Chronos.lean"

REQUIRED_DEFINITIONS = [
    "Phi(r) = -GM/r",
    "g(r) = GM/r^2",
    "v_esc = sqrt(2GM/R)",
    "Delta_g approximately equals -(2g0/R)x",
    "K_g = 2g0/R",
    "tidal signature: radial stretch and transverse compression",
]

REQUIRED_BOUNDARIES = [
    "symbolic response model only",
    "no empirical validation",
    "no real likelihood evidence",
    "no independent replication result",
    "no physical validation",
    "no literal gravity elasticity",
    "no standard GR failure",
    "no new physics",
    "no dark matter replacement",
    "no Lambda-CDM failure",
    "no unrestricted Chronos-RR",
    "no unrestricted H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]

REQUIRED_LEAN_TOKENS = [
    "import Chronos.Frontier.YtRGravityElasticIndependentReplicationGate",
    "structure YtRGravityElasticResponseModel",
    "def ytrGravityElasticResponseModel",
    "def ytrGravityElasticResponseApproximation",
    "def ytrGravityElasticTidalSignature",
    "theorem ytr_gravity_elastic_response_coefficient_law",
    "theorem ytr_gravity_elastic_escape_scale_law",
    "theorem ytr_gravity_elastic_response_reference_radius_positive",
    "theorem ytr_gravity_elastic_response_model_named",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    for path in [ART, DOC, LEAN, CHRONOS]:
        require(path.exists(), f"missing required file: {path}")

    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    lean = LEAN.read_text()
    chronos = CHRONOS.read_text()

    require(
        data.get("id") == "YTR_GRAVITY_ELASTIC_RESPONSE_MODEL_2026_05_29",
        "artifact id mismatch",
    )
    require(
        data.get("status") == "SYMBOLIC_RESPONSE_MODEL_ONLY_NO_PHYSICAL_VALIDATION",
        "artifact status mismatch",
    )
    require(
        data.get("theorem_object") == "YtRGravityElasticResponseModel",
        "artifact theorem_object mismatch",
    )
    require(
        "YTR_GRAVITY_ELASTIC_INDEPENDENT_REPLICATION_GATE_2026_05_29"
        in data.get("depends_on", []),
        "missing dependency on independent replication gate",
    )

    for token in REQUIRED_DEFINITIONS:
        require(token in data.get("definitions", []), f"artifact missing definition: {token}")

    for token in REQUIRED_BOUNDARIES:
        require(token in data.get("boundary", []), f"artifact missing boundary token: {token}")
        require(token in doc, f"doc missing boundary token: {token}")

    for token in REQUIRED_LEAN_TOKENS:
        require(token in lean, f"Lean file missing token: {token}")

    require(
        "import Chronos.Frontier.YtRGravityElasticResponseModel" in chronos,
        "Chronos.lean missing import",
    )

    print("YTR_GRAVITY_ELASTIC_RESPONSE_MODEL_OK")


if __name__ == "__main__":
    main()
