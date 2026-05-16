#!/usr/bin/env python3
import json
import sys
from pathlib import Path

STATUS = "CONDITIONAL_RESTRICTED_COLLAPSE_GATE_ONLY"
REQUIRED_ASSUMPTIONS = ["A1", "A2", "A3", "A4", "A5", "A6"]

REQUIRED_NON_CLAIMS = [
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted QL_CollapseGate",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "unrestricted nonspherical collapse exclusion",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP or any Clay problem",
]

FORBIDDEN_OVERCLAIMS = [
    "proves Cosmic Censorship",
    "proved Cosmic Censorship",
    "proves the Hoop Conjecture",
    "proved the Hoop Conjecture",
    "unconditional QL_CollapseGate",
    "unrestricted QL_CollapseGate is proved",
    "unconditional UniversalBoundaryCompactness",
    "solves P vs NP",
    "solves a Clay problem",
    "proves unrestricted Chronos-RR",
    "proves H4.1/FGL",
    "THE FIVE ASSUMPTIONS"
]

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)

def ok(message: str) -> None:
    print(f"PASS: {message}")

def load_artifact(path: Path) -> dict:
    if not path.exists():
        fail(f"artifact not found: {path}")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")

def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: verify_conditional_ql_collapse_gate.py <artifact.json>")

    path = Path(sys.argv[1])
    artifact = load_artifact(path)
    raw = json.dumps(artifact, sort_keys=True)

    if artifact.get("status") != STATUS:
        fail("incorrect status label")
    ok("status label")

    if artifact.get("assumptions_heading") != "THE SIX ASSUMPTIONS":
        fail("assumptions heading must be THE SIX ASSUMPTIONS")
    ok("assumptions heading")

    assumptions = artifact.get("assumptions")
    if not isinstance(assumptions, list):
        fail("assumptions must be a list")
    if len(assumptions) != 6:
        fail(f"expected exactly 6 assumptions, found {len(assumptions)}")

    labels = [a.get("label") for a in assumptions]
    if labels != REQUIRED_ASSUMPTIONS:
        fail(f"assumption labels must be {REQUIRED_ASSUMPTIONS}, found {labels}")
    ok("six assumptions A1--A6")

    for assumption in assumptions:
        label = assumption.get("label")
        status = str(assumption.get("status", ""))
        if label == "A3":
            if status != "OPEN_CONJECTURE_ASSUMED":
                fail("A3 must be OPEN_CONJECTURE_ASSUMED")
        elif status != "ASSUMPTION":
            fail(f"{label} must be marked ASSUMPTION")
    ok("all assumptions marked correctly")

    a3 = assumptions[2]
    if a3.get("label") != "A3":
        fail("A3 must be weak cosmic censorship")
    if a3.get("status") != "OPEN_CONJECTURE_ASSUMED":
        fail("A3 must be OPEN_CONJECTURE_ASSUMED")
    ok("A3 is assumed open conjecture")

    a4 = assumptions[3]
    if a4.get("label") != "A4":
        fail("A4 missing")
    if a4.get("replaces") != "general Hoop Conjecture":
        fail("A4 must replace, not prove, the general Hoop Conjecture")
    ok("A4 replaces Hoop Conjecture")

    domain = artifact.get("domain", {})
    if domain.get("symbol") != "D_sp":
        fail("domain must be D_sp")
    if "short-pulse" not in domain.get("description", ""):
        fail("domain description must restrict to short-pulse")
    ok("D_sp domain restriction")

    theorem = artifact.get("theorem", {})
    if theorem.get("conditional") is not True:
        fail("theorem must be conditional")
    if theorem.get("restricted") is not True:
        fail("theorem must be restricted")
    ok("conditional restricted theorem structure")

    if artifact.get("matter_model") != "vacuum Einstein":
        fail("matter model must be vacuum Einstein")
    ok("vacuum Einstein matter model")

    non_claims = artifact.get("non_claims", [])
    for claim in REQUIRED_NON_CLAIMS:
        if claim not in non_claims:
            fail(f"missing non-claim: {claim}")
    ok("all required non-claims")

    for token in FORBIDDEN_OVERCLAIMS:
        if token in raw:
            fail(f"forbidden overclaim token present: {token}")
    ok("forbidden overclaims absent")

    files = artifact.get("files", {})
    for key in ("lean", "artifact", "verifier", "pytest"):
        if key not in files:
            fail(f"missing file reference: {key}")
    ok("file references")

    print("VERIFICATION PASSED")

if __name__ == "__main__":
    main()
