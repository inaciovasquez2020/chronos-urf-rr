#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(".")
ARTIFACT = ROOT / "artifacts/chronos/gravity_open_problem_lock_2026_05_16.json"
LEAN = ROOT / "lean/Chronos/Frontier/GravityOpenProblemLock.lean"
STATUS = ROOT / "docs/status/GRAVITY_OPEN_PROBLEM_LOCK_2026_05_16.md"

REQUIRED_LOCK_IDS = {
    "A3",
    "A4",
    "QL_COLLAPSE_GATE",
    "BOUNDARY_COMPACTNESS",
}

REQUIRED_PHRASES = [
    "OPEN_PROBLEM_LOCK_ONLY",
    "A3 remains an assumption",
    "A4 remains a restricted trapped-surface replacement",
    "QL_CollapseGate remains conditional on A1--A6",
    "UniversalBoundaryCompactness remains replaced by BoundaryCompactness(F_Λ)",
]

FORBIDDEN_PROMOTION_PHRASES = [
    "Cosmic Censorship is proved",
    "Hoop Conjecture is proved",
    "unrestricted QL_CollapseGate is proved",
    "unrestricted UniversalBoundaryCompactness is proved",
    "unrestricted Chronos-RR is proved",
    "H4.1/FGL is proved",
    "P vs NP is proved",
    "Clay problem is solved",
]

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")

def main() -> None:
    require(ARTIFACT.exists(), f"missing artifact: {ARTIFACT}")
    require(LEAN.exists(), f"missing Lean file: {LEAN}")
    require(STATUS.exists(), f"missing status doc: {STATUS}")

    artifact = json.loads(ARTIFACT.read_text())
    lean = LEAN.read_text()
    status = STATUS.read_text()
    combined = "\n".join([json.dumps(artifact, sort_keys=True), lean, status])

    require(artifact.get("status") == "OPEN_PROBLEM_LOCK_ONLY", "wrong status")

    lock_ids = {item.get("id") for item in artifact.get("locks", [])}
    require(REQUIRED_LOCK_IDS <= lock_ids, f"missing locks: {REQUIRED_LOCK_IDS - lock_ids}")

    for phrase in REQUIRED_PHRASES:
        require(phrase in combined, f"missing phrase: {phrase}")

    for phrase in FORBIDDEN_PROMOTION_PHRASES:
        require(phrase not in combined, f"forbidden promotion phrase present: {phrase}")

    require("gravityOpenProblemLock" in lean, "missing Lean lock object")
    require("gravity_open_problem_lock_preserves_A3" in lean, "missing A3 theorem")
    require("gravity_open_problem_lock_preserves_A4" in lean, "missing A4 theorem")
    require("gravity_open_problem_lock_preserves_conditional_gate" in lean, "missing QL theorem")
    require("gravity_open_problem_lock_preserves_boundary_replacement" in lean, "missing boundary theorem")

    print("Gravity open problem lock verified.")

if __name__ == "__main__":
    main()
