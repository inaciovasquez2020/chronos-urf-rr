#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ARTIFACT = Path("artifacts/external_validation/selected_domain_repair_field_package_bridge_rollup_2026_06_25.json")

EXPECTED_SHORTS = ["ca298ce2", "8ddd5c8f", "2b1003ab", "86ec2e49", "f24dd313"]

EXPECTED_SUBJECTS = {
    "ca298ce2": "lean: expose selected domain repair target from field package",
    "8ddd5c8f": "docs: record selected domain repair field package bridge",
    "2b1003ab": "tools: verify selected domain repair field package bridge",
    "86ec2e49": "tests: cover selected domain repair field package bridge verifier",
    "f24dd313": "docs: add selected domain repair field package status",
}

EXPECTED_NON_CLAIMS = [
    "does not push branch",
    "does not add a new Lean theorem",
    "does not construct a field-package provider",
    "does not prove selected-domain representability",
    "does not prove normalization independently of the package",
]

def fail(message: str) -> None:
    raise SystemExit(f"SELECTED_DOMAIN_REPAIR_FIELD_PACKAGE_BRIDGE_ROLLUP_2026_06_25_FAIL: {message}")

def git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()

def main() -> None:
    if not ARTIFACT.is_file():
        fail(f"missing artifact {ARTIFACT}")

    data = json.loads(ARTIFACT.read_text())

    if data.get("artifact") != "SELECTED_DOMAIN_REPAIR_FIELD_PACKAGE_BRIDGE_ROLLUP_2026_06_25":
        fail("artifact marker mismatch")
    if data.get("repository") != "chronos-urf-rr":
        fail("repository mismatch")
    if data.get("branch") != "internal/selected-domain-repair-theorem-surface-20260625":
        fail("branch mismatch")
    if data.get("range") != "ca298ce2..f24dd313 inclusive":
        fail("range mismatch")
    if data.get("lean_target") != "Chronos.Frontier.H4_1_FGL_SelectedDomainRestriction":
        fail("lean_target mismatch")
    if data.get("non_claims") != EXPECTED_NON_CLAIMS:
        fail("non_claims mismatch")

    commits = data.get("commits")
    if not isinstance(commits, list):
        fail("commits is not a list")
    if [entry.get("short") for entry in commits] != EXPECTED_SHORTS:
        fail("commit short list mismatch")

    for entry in commits:
        short = entry["short"]
        commit = entry.get("commit")

        if not isinstance(commit, str) or not commit.startswith(short):
            fail(f"commit hash prefix mismatch for {short}")
        if entry.get("subject") != EXPECTED_SUBJECTS[short]:
            fail(f"artifact subject mismatch for {short}")
        if not entry.get("validated_object"):
            fail(f"missing validated_object for {short}")
        validation = entry.get("validation")
        if not isinstance(validation, list) or not validation:
            fail(f"missing validation list for {short}")

    print("SELECTED_DOMAIN_REPAIR_FIELD_PACKAGE_BRIDGE_ROLLUP_2026_06_25_OK")

if __name__ == "__main__":
    main()
