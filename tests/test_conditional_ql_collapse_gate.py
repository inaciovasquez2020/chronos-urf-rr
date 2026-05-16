import json
import subprocess
import sys
from pathlib import Path

ARTIFACT = Path("artifacts/chronos/conditional_ql_collapse_gate_2026_05_16.json")

def load_artifact() -> dict:
    return json.loads(ARTIFACT.read_text())

def test_status_label_is_conditional_restricted():
    a = load_artifact()
    assert a["status"] == "CONDITIONAL_RESTRICTED_COLLAPSE_GATE_ONLY"

def test_assumption_heading_is_six_not_five():
    a = load_artifact()
    assert a["assumptions_heading"] == "THE SIX ASSUMPTIONS"
    assert "THE FIVE ASSUMPTIONS" not in json.dumps(a)

def test_exactly_six_assumptions():
    a = load_artifact()
    assert [x["label"] for x in a["assumptions"]] == ["A1", "A2", "A3", "A4", "A5", "A6"]

def test_domain_is_short_pulse_dsp():
    a = load_artifact()
    assert a["domain"]["symbol"] == "D_sp"
    assert "short-pulse" in a["domain"]["description"]

def test_a3_cosmic_censorship_is_assumption_not_proof():
    a = load_artifact()
    A3 = a["assumptions"][2]
    assert A3["label"] == "A3"
    assert A3["status"] == "OPEN_CONJECTURE_ASSUMED"
    assert "Cosmic Censorship" in a["non_claims"]

def test_a4_replaces_hoop_conjecture_not_proves_it():
    a = load_artifact()
    A4 = a["assumptions"][3]
    assert A4["label"] == "A4"
    assert A4["replaces"] == "general Hoop Conjecture"
    assert "Hoop Conjecture" in a["non_claims"]

def test_theorem_is_conditional_and_restricted():
    a = load_artifact()
    assert a["theorem"]["conditional"] is True
    assert a["theorem"]["restricted"] is True

def test_matter_model_is_vacuum_einstein():
    a = load_artifact()
    assert a["matter_model"] == "vacuum Einstein"

def test_required_non_claims_present():
    a = load_artifact()
    required = {
        "unrestricted UniversalBoundaryCompactness",
        "unrestricted QL_CollapseGate",
        "Cosmic Censorship",
        "Hoop Conjecture",
        "unrestricted nonspherical collapse exclusion",
        "unrestricted Chronos-RR",
        "H4.1/FGL",
        "P vs NP or any Clay problem",
    }
    assert required.issubset(set(a["non_claims"]))

def test_forbidden_overclaim_tokens_absent():
    a = load_artifact()
    raw = json.dumps(a)
    forbidden = [
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
        "THE FIVE ASSUMPTIONS",
    ]
    for token in forbidden:
        assert token not in raw

def test_file_references_present():
    a = load_artifact()
    assert a["files"]["lean"].endswith("ConditionalQLCollapseGate_Objects.lean")
    assert a["files"]["artifact"].endswith("conditional_ql_collapse_gate_2026_05_16.json")
    assert a["files"]["verifier"].endswith("verify_conditional_ql_collapse_gate.py")
    assert a["files"]["pytest"].endswith("test_conditional_ql_collapse_gate.py")

def test_verifier_passes():
    subprocess.run(
        [
            sys.executable,
            "tools/verify_conditional_ql_collapse_gate.py",
            str(ARTIFACT),
        ],
        check=True,
    )
