#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/R1R2R3IsolatedTargetsConditionalClosure.lean"
ART = ROOT / "artifacts/chronos/r1_r2_r3_isolated_targets_conditional_closure_2026_05_24.json"
DOC = ROOT / "docs/status/R1_R2_R3_ISOLATED_TARGETS_CONDITIONAL_CLOSURE_2026_05_24.md"
CHECKER = ROOT / "tools/check_long_chord_witness_obstruction.py"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

REQUIRED_LEAN = [
    "def LongChordExclusionProofTarget : Prop := True",
    "def DiameterSeparationFillingObstructionProofTarget : Prop := True",
    "opaque UniformLocalTypeCapacityProofTarget : Prop",
    "opaque NonFactorisationProofTarget : Prop",
    "def RepositoryNativeR1R2R3InstanceTarget : Prop :=",
    "theorem repository_native_r1_r2_r3_binding_conditional_closure",
    "def RepositoryNativeR1R2R3BindingClosureConditionalTarget : Prop :=",
    "def RepositoryNativeR1R2R3BindingClosureMissingObject : Prop :=",
]

BOUNDARY = [
    "native R1/R2/R3 instance",
    "LongChordExclusion",
    "DiameterSeparationFillingObstruction",
    "UniformLocalTypeCapacity",
    "NON_FACTORISATION",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

def require(cond, msg):
    if not cond:
        raise AssertionError(msg)

def main():
    for path in [LEAN, ART, DOC, CHECKER, ROOT_IMPORT]:
        require(path.exists(), f"missing {path}")

    lean = LEAN.read_text()
    for token in REQUIRED_LEAN:
        require(token in lean, f"missing Lean token: {token}")

    require("import Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure" in ROOT_IMPORT.read_text(),
            "missing root Chronos import")

    data = json.loads(ART.read_text())
    require(data["status"] == "CONDITIONAL_COMPOSITION_ONLY_FRONTIER_OPEN", "wrong artifact status")
    require(data["missing_object"] == "RepositoryNativeR1R2R3BindingClosureMissingObject", "wrong missing object")
    for token in BOUNDARY:
        require(token in data["does_not_prove"], f"missing artifact boundary: {token}")

    doc = DOC.read_text()
    require("Status: `CONDITIONAL_COMPOSITION_ONLY_FRONTIER_OPEN`" in doc, "missing doc status")
    for token in BOUNDARY:
        require(token in doc, f"missing doc boundary: {token}")

    checker = CHECKER.read_text()
    require("LONG_CHORD_WITNESS_CHECK_OK" in checker, "checker lacks success token")
    require("FINITE_LONG_CHORD_WITNESS_PACKET" in checker, "checker lacks packet status token")

    print("R1_R2_R3_ISOLATED_TARGETS_CONDITIONAL_CLOSURE_OK")

if __name__ == "__main__":
    main()
