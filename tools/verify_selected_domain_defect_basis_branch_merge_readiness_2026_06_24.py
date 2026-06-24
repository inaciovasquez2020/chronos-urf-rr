#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/external_validation/selected_domain_defect_basis_branch_merge_readiness_2026_06_24.json"
DOC = ROOT / "docs/status/SELECTED_DOMAIN_DEFECT_BASIS_BRANCH_MERGE_READINESS_2026_06_24.md"

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["target"] == "SELECTED_DOMAIN_DEFECT_BASIS_BRANCH_MERGE_READINESS_2026_06_24"
    assert data["status"] == "merge_ready_after_local_validation"
    assert data["branch"] == "docs/selected-domain-defect-basis-2026-06-24"

    for token in [
        "lake build Chronos",
        "python3 -m pytest -q",
        "git diff --check",
        "renamed forbidden diameter helper theorem prefixes",
        "renamed forbidden uniform helper theorem prefix",
        "CONDITIONAL_ON_FourBridgesSource_OR_ACTIVE_URF11BridgeRegistry",
        "NO_ACTIVE_URF11BridgeRegistry_INSTANCE_DECLARED",
        "NO_UNCONDITIONAL_NATIVE_R2_R3_SOURCE_COMPATIBILITY_CLOSURE",
        "NO_FINAL_CLOSURE_CLAIM",
    ]:
        assert token in doc
        assert token in json.dumps(data)

    print("SELECTED_DOMAIN_DEFECT_BASIS_BRANCH_MERGE_READINESS_2026_06_24_OK")

if __name__ == "__main__":
    main()
