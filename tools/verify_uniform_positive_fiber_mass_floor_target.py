#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/UniformPositiveFiberMassFloorTarget.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/uniform_positive_fiber_mass_floor_target_2026_05_18.json"
DOC = ROOT / "docs/status/UNIFORM_POSITIVE_FIBER_MASS_FLOOR_TARGET_2026_05_18.md"

REQUIRED_LEAN = [
    "structure FiberMassDomain",
    "def UniformPositiveFiberMassFloor",
    "def NoUniformPositiveFiberMassFloorCountermodel",
    "inductive UniformPositiveFiberMassSinkResolution",
    "theorem uniform_positive_floor_closure_resolves_sink",
    "theorem no_uniform_positive_floor_countermodel_resolves_sink",
    "theorem countermodel_excludes_uniform_positive_floor",
    "def UniformPositiveFiberMassFloorTargetStatus",
]

REQUIRED_DOC = [
    "Status: `OPEN_TARGET_SURFACE_ONLY`",
    "Global verdict preserved: `OPEN`",
    "`UniformPositiveFiberMassFloor`",
    "`NoUniformPositiveFiberMassFloorCountermodel`",
    "`countermodel_excludes_uniform_positive_floor`",
    "Does not prove:",
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
    "existence of UniformPositiveFiberMassFloor is proved",
]

def assert_no_proof_holes(text: str) -> None:
    bad = re.findall(r"\b(sorry|admit|axiom)\b", text)
    assert not bad, f"proof-hole tokens present: {bad}"

def main() -> None:
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert ARTIFACT.exists(), f"missing artifact: {ARTIFACT}"
    assert DOC.exists(), f"missing doc: {DOC}"

    lean = LEAN.read_text()
    root_lean = ROOT_LEAN.read_text()
    artifact_text = ARTIFACT.read_text()
    doc = DOC.read_text()
    data = json.loads(artifact_text)

    assert_no_proof_holes(lean)

    for phrase in REQUIRED_LEAN:
        assert phrase in lean

    assert "import Chronos.Frontier.UniformPositiveFiberMassFloorTarget" in root_lean

    assert data["status"] == "OPEN_TARGET_SURFACE_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False
    assert data["sink_id"] == "uniform_positive_mass_or_countermodel"
    assert "countermodel_excludes_uniform_positive_floor" in data["proved_surface_theorems"]
    assert "existence of UniformPositiveFiberMassFloor" in data["boundary"]["does_not_prove"]

    for phrase in REQUIRED_DOC:
        assert phrase in doc

    combined = lean + "\n" + artifact_text + "\n" + doc
    for phrase in FORBIDDEN:
        assert phrase not in combined

    print("Uniform positive fiber-mass floor target verified.")

if __name__ == "__main__":
    main()
