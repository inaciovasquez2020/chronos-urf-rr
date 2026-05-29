#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ART = ROOT / "artifacts/chronos/ytr_gravity_elastic_nontriviality_certificate_2026_05_29.json"
DOC = ROOT / "docs/status/YTR_GRAVITY_ELASTIC_NONTRIVIALITY_CERTIFICATE_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/YtRGravityElasticNontrivialityCertificate.lean"
CHRONOS = ROOT / "lean/Chronos.lean"

REQUIRED_BOUNDARIES = [
    "synthetic nontriviality certificate gate only",
    "no empirical validation",
    "no real likelihood evidence",
    "no independent replication",
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
    "import Chronos.Frontier.YtRGravityElasticStandardGRComparison",
    "structure YtRGravityElasticNontrivialityCertificate",
    "def ytrMetricElasticNontrivialityCertificate",
    "def ytrTidalRestoringNontrivialityCertificate",
    "theorem ytr_metric_elastic_nontriviality_certificate_separates",
    "theorem ytr_tidal_restoring_nontriviality_certificate_separates",
    "theorem ytr_gravity_elastic_nontriviality_certificate_gate_nonempty",
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
        data.get("id") == "YTR_GRAVITY_ELASTIC_NONTRIVIALITY_CERTIFICATE_2026_05_29",
        "artifact id mismatch",
    )
    require(
        data.get("status") == "SYNTHETIC_NONTRIVIALITY_CERTIFICATE_GATE_ONLY",
        "artifact status mismatch",
    )
    require(
        data.get("theorem_object") == "YtRGravityElasticNontrivialityCertificate",
        "artifact theorem_object mismatch",
    )
    require(
        "YTR_GRAVITY_ELASTIC_STANDARD_GR_COMPARISON_2026_05_29"
        in data.get("depends_on", []),
        "missing dependency on standard-GR comparison gate",
    )

    targets = data.get("certificate_targets", [])
    require(len(targets) == 2, "expected exactly two certificate targets")
    for target in targets:
        require(
            target.get("standard_gr_reference") != target.get("ytr_candidate"),
            f"target lacks synthetic separation: {target}",
        )
        require(
            target.get("certificate_kind") == "synthetic_separation_witness",
            f"unexpected certificate kind: {target}",
        )

    boundary = data.get("boundary", [])
    for token in REQUIRED_BOUNDARIES:
        require(token in boundary, f"artifact missing boundary token: {token}")
        require(token in doc, f"doc missing boundary token: {token}")

    for token in REQUIRED_LEAN_TOKENS:
        require(token in lean, f"Lean file missing token: {token}")

    require(
        "import Chronos.Frontier.YtRGravityElasticNontrivialityCertificate"
        in chronos,
        "Chronos.lean missing import",
    )

    print("YTR_GRAVITY_ELASTIC_NONTRIVIALITY_CERTIFICATE_OK")


if __name__ == "__main__":
    main()
