#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ART = ROOT / "artifacts/chronos/ytr_gravity_elastic_independent_replication_gate_2026_05_29.json"
DOC = ROOT / "docs/status/YTR_GRAVITY_ELASTIC_INDEPENDENT_REPLICATION_GATE_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/YtRGravityElasticIndependentReplicationGate.lean"
CHRONOS = ROOT / "lean/Chronos.lean"

REQUIRED_CONDITIONS = [
    "requires independent operator",
    "requires clean environment",
    "requires artifact digest match",
    "requires result agreement",
]

REQUIRED_BOUNDARIES = [
    "independent replication gate only",
    "no independent replication",
    "no empirical validation",
    "no real likelihood evidence",
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
    "import Chronos.Frontier.YtRGravityElasticNontrivialityCertificate",
    "structure YtRGravityElasticIndependentReplicationGate",
    "def ytrGravityElasticIndependentReplicationGate",
    "theorem ytr_gravity_elastic_independent_replication_requires_operator",
    "theorem ytr_gravity_elastic_independent_replication_requires_clean_environment",
    "theorem ytr_gravity_elastic_independent_replication_requires_digest_match",
    "theorem ytr_gravity_elastic_independent_replication_requires_result_agreement",
    "theorem ytr_gravity_elastic_independent_replication_gate_all_requirements",
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
        data.get("id") == "YTR_GRAVITY_ELASTIC_INDEPENDENT_REPLICATION_GATE_2026_05_29",
        "artifact id mismatch",
    )
    require(
        data.get("status") == "INDEPENDENT_REPLICATION_GATE_ONLY_NO_REPLICATION",
        "artifact status mismatch",
    )
    require(
        data.get("theorem_object") == "YtRGravityElasticIndependentReplicationGate",
        "artifact theorem_object mismatch",
    )
    require(
        "YTR_GRAVITY_ELASTIC_NONTRIVIALITY_CERTIFICATE_2026_05_29"
        in data.get("depends_on", []),
        "missing dependency on nontriviality certificate gate",
    )

    for token in REQUIRED_CONDITIONS:
        require(token in data.get("required_conditions", []), f"artifact missing condition: {token}")
        require(token in doc, f"doc missing condition: {token}")

    for token in REQUIRED_BOUNDARIES:
        require(token in data.get("boundary", []), f"artifact missing boundary token: {token}")
        require(token in doc, f"doc missing boundary token: {token}")

    for token in REQUIRED_LEAN_TOKENS:
        require(token in lean, f"Lean file missing token: {token}")

    require(
        "import Chronos.Frontier.YtRGravityElasticIndependentReplicationGate"
        in chronos,
        "Chronos.lean missing import",
    )

    print("YTR_GRAVITY_ELASTIC_INDEPENDENT_REPLICATION_GATE_OK")


if __name__ == "__main__":
    main()
