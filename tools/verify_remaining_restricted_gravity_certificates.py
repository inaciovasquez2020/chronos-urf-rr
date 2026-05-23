#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OBJECTS = [
    {
        "artifact": ROOT / "artifacts/chronos/restricted_continuation_until_threshold_certificate_2026_05_23.json",
        "status": ROOT / "docs/status/RESTRICTED_CONTINUATION_UNTIL_THRESHOLD_CERTIFICATE_2026_05_23.md",
        "lean": ROOT / "lean/Chronos/Frontier/RestrictedContinuationUntilThresholdCertificate.lean",
        "artifact_name": "RESTRICTED_CONTINUATION_UNTIL_THRESHOLD_CERTIFICATE",
        "status_name": "RESTRICTED_CONTINUATION_UNTIL_THRESHOLD_CERTIFICATE_ONLY_NO_GRAVITY_CLOSURE",
        "lean_module": "Chronos.Frontier.RestrictedContinuationUntilThresholdCertificate",
        "tokens": [
            "structure RestrictedContinuationDatum",
            "def ContinuationUntilThreshold",
            "structure RestrictedContinuationUntilThresholdCertificate",
            "theorem restricted_continuation_until_threshold_certificate",
            "theorem extends_past_of_restricted_continuation_certificate"
        ],
        "boundaries": [
            "analytic Einstein-matter bootstrap package",
            "matter-coupling compatibility",
            "constraint propagation",
            "energy-condition preservation",
            "restricted collapse-gate trigger",
            "gravity closure",
            "Chronos-RR",
            "H4.1/FGL",
            "P vs NP",
            "any Clay problem"
        ]
    },
    {
        "artifact": ROOT / "artifacts/chronos/restricted_collapse_gate_trigger_certificate_2026_05_23.json",
        "status": ROOT / "docs/status/RESTRICTED_COLLAPSE_GATE_TRIGGER_CERTIFICATE_2026_05_23.md",
        "lean": ROOT / "lean/Chronos/Frontier/RestrictedCollapseGateTriggerCertificate.lean",
        "artifact_name": "RESTRICTED_COLLAPSE_GATE_TRIGGER_CERTIFICATE",
        "status_name": "RESTRICTED_COLLAPSE_GATE_TRIGGER_CERTIFICATE_ONLY_NO_GRAVITY_CLOSURE",
        "lean_module": "Chronos.Frontier.RestrictedCollapseGateTriggerCertificate",
        "tokens": [
            "structure RestrictedCollapseGateTriggerDatum",
            "def RestrictedCollapseGateTriggers",
            "structure RestrictedCollapseGateTriggerCertificate",
            "theorem restricted_collapse_gate_trigger_certificate",
            "theorem collapse_gate_at_trigger_time_of_certificate"
        ],
        "boundaries": [
            "analytic Einstein-matter bootstrap package",
            "matter-coupling compatibility",
            "constraint propagation",
            "energy-condition preservation",
            "continuation until collapse threshold",
            "gravity closure",
            "Chronos-RR",
            "H4.1/FGL",
            "P vs NP",
            "any Clay problem"
        ]
    },
    {
        "artifact": ROOT / "artifacts/chronos/restricted_einstein_matter_bootstrap_package_certificate_2026_05_23.json",
        "status": ROOT / "docs/status/RESTRICTED_EINSTEIN_MATTER_BOOTSTRAP_PACKAGE_CERTIFICATE_2026_05_23.md",
        "lean": ROOT / "lean/Chronos/Frontier/RestrictedEinsteinMatterBootstrapPackageCertificate.lean",
        "artifact_name": "RESTRICTED_EINSTEIN_MATTER_BOOTSTRAP_PACKAGE_CERTIFICATE",
        "status_name": "RESTRICTED_EINSTEIN_MATTER_BOOTSTRAP_PACKAGE_CERTIFICATE_ONLY_NO_GRAVITY_CLOSURE",
        "lean_module": "Chronos.Frontier.RestrictedEinsteinMatterBootstrapPackageCertificate",
        "tokens": [
            "structure RestrictedEinsteinMatterBootstrapDatum",
            "def RestrictedEinsteinMatterBootstrapPackage",
            "structure RestrictedEinsteinMatterBootstrapPackageCertificate",
            "theorem restricted_einstein_matter_bootstrap_package_certificate",
            "theorem collapse_gate_of_restricted_bootstrap_package"
        ],
        "boundaries": [
            "analytic Einstein-matter bootstrap package",
            "concrete analytic Einstein-matter estimate package",
            "finite continuation norm",
            "bootstrap bounds",
            "concentration monotonicity",
            "threshold crossing",
            "gravity closure",
            "Chronos-RR",
            "H4.1/FGL",
            "P vs NP",
            "any Clay problem"
        ]
    }
]

def check_object(obj: dict[str, object]) -> None:
    artifact_path = obj["artifact"]
    status_path = obj["status"]
    lean_path = obj["lean"]

    assert isinstance(artifact_path, Path)
    assert isinstance(status_path, Path)
    assert isinstance(lean_path, Path)

    assert artifact_path.exists(), artifact_path
    assert status_path.exists(), status_path
    assert lean_path.exists(), lean_path

    data = json.loads(artifact_path.read_text())
    status = status_path.read_text()
    lean = lean_path.read_text()

    assert data["artifact"] == obj["artifact_name"]
    assert data["status"] == obj["status_name"]
    assert data["lean_module"] == obj["lean_module"]

    for token in obj["tokens"]:
        assert token in lean, token

    for boundary in obj["boundaries"]:
        assert boundary in data["does_not_prove"], boundary
        assert boundary in status, boundary
        assert boundary in lean, boundary

    blob = (status + "\n" + lean).lower()
    assert "gravity solved" not in blob
    assert "clay solved" not in blob
    assert "p vs np solved" not in blob

def main() -> None:
    for obj in OBJECTS:
        check_object(obj)

    package = json.loads((ROOT / "artifacts/chronos/restricted_einstein_matter_bootstrap_package_certificate_2026_05_23.json").read_text())
    assert package["minimal_missing_lemma"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE"

    print("Remaining restricted gravity certificates verification OK.")
    print("Statuses:")
    for obj in OBJECTS:
        data = json.loads(obj["artifact"].read_text())
        print("-", data["status"])

if __name__ == "__main__":
    main()
