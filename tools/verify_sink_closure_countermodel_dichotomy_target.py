#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/SinkClosureCountermodelDichotomyTarget.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/sink_closure_countermodel_dichotomy_target_2026_05_18.json"
DOC = ROOT / "docs/status/SINK_CLOSURE_COUNTERMODEL_DICHOTOMY_TARGET_2026_05_18.md"

REQUIRED_LEAN = [
    "structure SinkResolutionProblem",
    "def SinkResolved",
    "def CountermodelOrClosureDichotomyTarget",
    "def CountermodelOrClosureDichotomyFailure",
    "theorem closure_certificate_resolves_sink",
    "theorem countermodel_certificate_resolves_sink",
    "theorem unresolved_sink_excludes_dichotomy",
    "def SinkClosureCountermodelDichotomyTargetStatus",
]

REQUIRED_DOC = [
    "Status: `OPEN_DICHOTOMY_TARGET_SURFACE_ONLY`",
    "Global verdict preserved: `OPEN`",
    "`CountermodelOrClosureDichotomyTarget`",
    "`CountermodelOrClosureDichotomyFailure`",
    "`unresolved_sink_excludes_dichotomy`",
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
    "CountermodelOrClosureDichotomyTarget is proved",
]

def main() -> None:
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert ARTIFACT.exists(), f"missing artifact: {ARTIFACT}"
    assert DOC.exists(), f"missing doc: {DOC}"

    lean = LEAN.read_text()
    root_lean = ROOT_LEAN.read_text()
    artifact_text = ARTIFACT.read_text()
    doc = DOC.read_text()
    data = json.loads(artifact_text)

    assert not re.search(r"\b(sorry|admit|axiom)\b", lean)

    for phrase in REQUIRED_LEAN:
        assert phrase in lean

    assert "import Chronos.Frontier.SinkClosureCountermodelDichotomyTarget" in root_lean

    assert data["status"] == "OPEN_DICHOTOMY_TARGET_SURFACE_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False
    assert data["sink_id"] == "countermodel_or_closure_dichotomy"
    assert "unresolved_sink_excludes_dichotomy" in data["proved_surface_theorems"]
    assert "CountermodelOrClosureDichotomyTarget" in data["boundary"]["does_not_prove"]

    for phrase in REQUIRED_DOC:
        assert phrase in doc

    combined = lean + "\n" + artifact_text + "\n" + doc
    for phrase in FORBIDDEN:
        assert phrase not in combined

    print("Sink closure/countermodel dichotomy target verified.")

if __name__ == "__main__":
    main()
