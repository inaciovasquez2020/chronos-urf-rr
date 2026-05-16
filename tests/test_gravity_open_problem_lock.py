import json
import subprocess
import sys
from pathlib import Path

ARTIFACT = Path("artifacts/chronos/gravity_open_problem_lock_2026_05_16.json")
STATUS = Path("docs/status/GRAVITY_OPEN_PROBLEM_LOCK_2026_05_16.md")
LEAN = Path("lean/Chronos/Frontier/GravityOpenProblemLock.lean")

def load_artifact():
    return json.loads(ARTIFACT.read_text())

def test_status_is_open_problem_lock_only():
    assert load_artifact()["status"] == "OPEN_PROBLEM_LOCK_ONLY"

def test_four_required_locks_present():
    locks = {x["id"] for x in load_artifact()["locks"]}
    assert {
        "A3",
        "A4",
        "QL_COLLAPSE_GATE",
        "BOUNDARY_COMPACTNESS",
    } <= locks

def test_a3_kept_as_assumption():
    status = STATUS.read_text()
    assert "A3 remains an assumption" in status

def test_a4_kept_as_restricted_replacement():
    status = STATUS.read_text()
    assert "A4 remains a restricted trapped-surface replacement" in status

def test_ql_gate_kept_conditional():
    status = STATUS.read_text()
    assert "QL_CollapseGate remains conditional on A1--A6" in status

def test_boundary_compactness_kept_as_replacement():
    status = STATUS.read_text()
    assert "UniversalBoundaryCompactness remains replaced by BoundaryCompactness(F_Λ)" in status

def test_lean_lock_theorems_present():
    lean = LEAN.read_text()
    assert "gravity_open_problem_lock_preserves_A3" in lean
    assert "gravity_open_problem_lock_preserves_A4" in lean
    assert "gravity_open_problem_lock_preserves_conditional_gate" in lean
    assert "gravity_open_problem_lock_preserves_boundary_replacement" in lean

def test_forbidden_promotion_phrases_absent():
    combined = "\n".join([
        ARTIFACT.read_text(),
        STATUS.read_text(),
        LEAN.read_text(),
    ])
    forbidden = [
        "Cosmic Censorship is proved",
        "Hoop Conjecture is proved",
        "unrestricted QL_CollapseGate is proved",
        "unrestricted UniversalBoundaryCompactness is proved",
        "unrestricted Chronos-RR is proved",
        "H4.1/FGL is proved",
        "P vs NP is proved",
        "Clay problem is solved",
    ]
    for phrase in forbidden:
        assert phrase not in combined

def test_verifier_passes():
    subprocess.run(
        [sys.executable, "tools/verify_gravity_open_problem_lock.py"],
        check=True,
    )
