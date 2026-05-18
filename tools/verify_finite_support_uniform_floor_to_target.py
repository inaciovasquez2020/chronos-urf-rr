#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/FiniteSupportUniformFloorToTarget.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/finite_support_uniform_floor_to_target_2026_05_18.json"
DOC = ROOT / "docs/status/FINITE_SUPPORT_UNIFORM_FLOOR_TO_TARGET_2026_05_18.md"

REQUIRED_LEAN = [
    "def FiniteSupportUniformFloorCertificate",
    "theorem finite_support_uniform_floor_to_target",
    "theorem finite_support_uniform_floor_resolves_sink",
    "def FiniteSupportUniformFloorToTargetStatus",
]

REQUIRED_DOC = [
    "Status: `FINITE_SUPPORT_TARGET_CLOSURE_ONLY`",
    "Global verdict preserved: `OPEN`",
    "`FiniteSupportUniformFloorCertificate`",
    "`finite_support_uniform_floor_to_target`",
    "`finite_support_uniform_floor_resolves_sink`",
    "Does not prove:",
    "finite-support-to-admissible-domain lift",
    "unrestricted `UniversalFiberEntropyGap`",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

FORBIDDEN = [
    "P vs NP is solved",
    "Clay problem is solved",
    "unrestricted Chronos-RR is proved",
    "unrestricted H4.1/FGL is proved",
    "unrestricted UniversalFiberEntropyGap is proved",
    "finite-support-to-admissible-domain lift is proved",
]

def main() -> None:
    assert LEAN.exists()
    assert ARTIFACT.exists()
    assert DOC.exists()

    lean = LEAN.read_text()
    root_lean = ROOT_LEAN.read_text()
    artifact_text = ARTIFACT.read_text()
    doc = DOC.read_text()
    data = json.loads(artifact_text)

    assert not re.search(r"\b(sorry|admit|axiom)\b", lean)

    for phrase in REQUIRED_LEAN:
        assert phrase in lean

    assert "import Chronos.Frontier.FiniteSupportUniformFloorToTarget" in root_lean

    assert data["status"] == "FINITE_SUPPORT_TARGET_CLOSURE_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False
    assert data["source"] == "uniform_positive_fiber_mass_floor_target_2026_05_18"
    assert "finite_support_uniform_floor_to_target" in data["proved_surface_theorems"]

    for phrase in REQUIRED_DOC:
        assert phrase in doc

    combined = lean + "\n" + artifact_text + "\n" + doc
    for phrase in FORBIDDEN:
        assert phrase not in combined

    print("Finite-support uniform floor to target verified.")

if __name__ == "__main__":
    main()
