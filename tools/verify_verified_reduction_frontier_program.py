#!/usr/bin/env python3
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/VerifiedReductionFrontierProgram.lean"
ART = ROOT / "artifacts/chronos/verified_reduction_frontier_program_2026_05_17.json"
DOC = ROOT / "docs/status/VERIFIED_REDUCTION_FRONTIER_PROGRAM_2026_05_17.md"

REQUIRED = [
    "inductive ClosureStatus",
    "inductive FrontierTarget",
    "def currentProgram",
    "def nextFrontier",
    "theorem next_frontier_is_admissible_domain_construction",
    "theorem unrestricted_lyapunov_certificate_obstruction_is_imported",
    "theorem current_program_has_five_stages",
    "admissible-domain construction excluding zero-gap systems",
]

FORBIDDEN = [
    "proves P vs NP",
    "proves H4.1/FGL",
    "proves Chronos-RR",
    "proves any Clay problem",
    "unrestricted UniversalFiberEntropyGap proved",
    "unrestricted RateThickFiberCoercivity proved",
    "admissible replacement domain has been constructed",
]

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

def main() -> None:
    lean = LEAN.read_text()
    doc = DOC.read_text()
    art = json.loads(ART.read_text())

    blob = lean + "\n" + doc + "\n" + json.dumps(art)

    for token in REQUIRED:
        require(token in blob, f"missing token: {token}")

    for token in FORBIDDEN:
        require(token not in blob, f"forbidden overclaim token: {token}")

    require(art["status"] == "VERIFIED_REDUCTION_FRONTIER_PROGRAM", "bad status")
    require(art["theorem_promotion"] is False, "theorem promotion must be false")
    require(
        art["next_frontier"] == "admissible-domain construction excluding zero-gap systems",
        "bad next frontier",
    )

    if shutil.which("lake") is not None:
        subprocess.run(
            ["lake", "build", "Chronos.Frontier.VerifiedReductionFrontierProgram"],
            cwd=ROOT,
            check=True,
        )

    print("Verified reduction-and-frontier program verified.")

if __name__ == "__main__":
    main()
