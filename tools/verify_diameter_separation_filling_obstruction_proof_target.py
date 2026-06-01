#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/diameter_separation_filling_obstruction_proof_target_2026_06_01.json")
DOC = Path("docs/status/DIAMETER_SEPARATION_FILLING_OBSTRUCTION_PROOF_TARGET_2026_06_01.md")

REQUIRED_INPUTS = {
    "diameter_separation_domain",
    "filling_operation_definition",
    "separation_invariant_definition",
    "positive_invariant_binding",
    "diameter_bound_binding",
    "obstruction_statement",
    "lean_checked_obstruction_proof_or_explicit_missing_lemma",
}

REQUIRED_NON_CLAIMS = {
    "no diameter separation filling obstruction proof supplied",
    "no R2 theorem closure",
    "no FourBridgesSourceSolved theorem closure",
    "no unrestricted non-factorization theorem",
    "no Chronos-RR closure",
    "no H4.1/FGL closure",
    "no P vs N claim",
    "no Clay-problem claim",
}

FORBIDDEN_CLAIMS = [
    "DIAMETER_SEPARATION_FILLING_OBSTRUCTION_CLOSED",
    "R2_THEOREM_CLOSED",
    "FOUR_BRIDGES_SOURCE_SOLVED",
    "UNRESTRICTED_NON_FACTORISATION_CLOSED",
    "CHRONOS_RR_CLOSED",
    "H4FGL_CLOSED",
    "P_VS_NP_CLOSED",
    "CLAY_CLOSED"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"

    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "DIAMETER_SEPARATION_FILLING_OBSTRUCTION_PROOF_TARGET_2026_06_01"
    assert data["object"] == "DIAMETER_SEPARATION_FILLING_OBSTRUCTION_PROOF_TARGET"
    assert data["status"] == "TARGET_OPEN_OBSTRUCTION_PROOF_NOT_SUPPLIED"
    assert data["decision"] == "PASS"

    assert data["proof_supplied"] is False
    assert data["diameter_separation_filling_obstruction_closed"] is False

    assert REQUIRED_INPUTS.issubset(set(data["required_inputs"]))
    assert REQUIRED_INPUTS.issubset(set(data["missing_inputs"]))
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in REQUIRED_INPUTS:
        assert token in doc

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "DIAMETER_SEPARATION_FILLING_OBSTRUCTION_PROOF_OR_EXPLICIT_MISSING_LEMMA"
    assert data["weakest_sufficient_next_input"] == "LeanCheckedDiameterSeparationFillingObstructionProofOrExplicitMissingLemma"

    print("DIAMETER_SEPARATION_FILLING_OBSTRUCTION_PROOF_TARGET_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "missing_input_count": len(data["missing_inputs"]),
        "non_claim_count": len(data["certified_non_claims"]),
        "next_admissible_object": data["next_admissible_object"],
        "weakest_sufficient_next_input": data["weakest_sufficient_next_input"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
