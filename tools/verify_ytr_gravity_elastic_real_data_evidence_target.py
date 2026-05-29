#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ART = ROOT / "artifacts/chronos/ytr_gravity_elastic_real_data_evidence_target_2026_05_29.json"
DOC = ROOT / "docs/status/YTR_GRAVITY_ELASTIC_REAL_DATA_EVIDENCE_TARGET_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/YtRGravityElasticRealDataEvidenceTarget.lean"
CHRONOS = ROOT / "lean/Chronos.lean"

REQUIRED_CONDITIONS = [
    "requires public dataset",
    "requires payload digest",
    "requires schema validation",
    "requires prediction vector",
    "requires standard-GR comparison",
    "requires Lambda-CDM comparison",
    "requires held-out evaluation",
    "requires uncertainty accounting",
]

REQUIRED_TARGETS = [
    "rotation-curve residual holdout target",
    "weak-lensing residual comparison target",
    "cosmological-background residual comparison target",
]

REQUIRED_BOUNDARIES = [
    "real-data evidence target only",
    "no real data evidence supplied",
    "no dataset payload bound",
    "no payload digest verified",
    "no schema validation executed",
    "no prediction vector executed on real data",
    "no standard-GR empirical comparison executed",
    "no Lambda-CDM empirical comparison executed",
    "no held-out evaluation executed",
    "no uncertainty accounting executed",
    "no empirical validation",
    "no real likelihood evidence",
    "no physical validation",
    "no independent replication result",
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
    "import Chronos.Frontier.YtRGravityElasticResponseModel",
    "structure YtRGravityElasticRealDataEvidenceTarget",
    "def ytrGravityElasticRealDataEvidenceTarget",
    "def ytrGravityElasticRealDataEvidenceCandidateTargets",
    "theorem ytr_gravity_elastic_real_data_requires_public_dataset",
    "theorem ytr_gravity_elastic_real_data_requires_payload_digest",
    "theorem ytr_gravity_elastic_real_data_requires_schema_validation",
    "theorem ytr_gravity_elastic_real_data_requires_prediction_vector",
    "theorem ytr_gravity_elastic_real_data_requires_standard_gr_comparison",
    "theorem ytr_gravity_elastic_real_data_requires_lambda_cdm_comparison",
    "theorem ytr_gravity_elastic_real_data_requires_heldout_evaluation",
    "theorem ytr_gravity_elastic_real_data_requires_uncertainty_accounting",
    "theorem ytr_gravity_elastic_real_data_evidence_not_supplied",
    "theorem ytr_gravity_elastic_real_data_candidate_target_count",
    "theorem ytr_gravity_elastic_real_data_target_all_requirements",
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
        data.get("id") == "YTR_GRAVITY_ELASTIC_REAL_DATA_EVIDENCE_TARGET_2026_05_29",
        "artifact id mismatch",
    )
    require(
        data.get("status") == "REAL_DATA_EVIDENCE_TARGET_ONLY_NO_EVIDENCE_SUPPLIED",
        "artifact status mismatch",
    )
    require(
        data.get("theorem_object") == "YtRGravityElasticRealDataEvidenceTarget",
        "artifact theorem_object mismatch",
    )
    require(
        "YTR_GRAVITY_ELASTIC_RESPONSE_MODEL_2026_05_29"
        in data.get("depends_on", []),
        "missing dependency on response model",
    )

    for token in REQUIRED_CONDITIONS:
        require(token in data.get("required_conditions", []), f"artifact missing condition: {token}")
        require(token in doc, f"doc missing condition: {token}")

    for token in REQUIRED_TARGETS:
        require(token in data.get("candidate_data_targets", []), f"artifact missing target: {token}")
        require(token in doc, f"doc missing target: {token}")

    for token in REQUIRED_BOUNDARIES:
        require(token in data.get("boundary", []), f"artifact missing boundary token: {token}")
        require(token in doc, f"doc missing boundary token: {token}")

    for token in REQUIRED_LEAN_TOKENS:
        require(token in lean, f"Lean file missing token: {token}")

    require(
        "import Chronos.Frontier.YtRGravityElasticRealDataEvidenceTarget"
        in chronos,
        "Chronos.lean missing import",
    )

    print("YTR_GRAVITY_ELASTIC_REAL_DATA_EVIDENCE_TARGET_OK")


if __name__ == "__main__":
    main()
