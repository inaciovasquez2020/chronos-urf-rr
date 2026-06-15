#!/usr/bin/env python3

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "artifacts/chronos/r1a_trivial_two_face_boundary_statement_surface_2026_06_15.json"

REQUIRED_EXACT_STATEMENT_KEYS = {
    "name",
    "formal_surface",
    "quantifiers",
    "hypotheses",
    "conclusion",
    "r1_dependency_role",
}

REQUIRED_NON_CLAIMS = {
    "does not prove R1a",
    "does not prove R1b",
    "does not prove R1c",
    "does not prove Long-Chord Exclusion Lemma",
    "does not prove FGL",
    "does not prove Chronos-RR",
    "does not prove P vs NP",
    "does not prove any Clay problem",
}

FORBIDDEN_TRUE_CLAIMS = {
    "proves_r1a",
    "proves_r1b",
    "proves_r1c",
    "proves_r1",
    "proves_r2",
    "proves_r3",
    "proves_fgl",
    "proves_chronos_rr",
    "proves_p_vs_np",
    "proves_any_clay_problem",
}

FORBIDDEN_OVERCLAIM_TOKENS = (
    "R1A_PROVED",
    "R1A_CLOSED",
    "R1_PROVED",
    "R1_CLOSED",
    "FGL_PROVED",
    "FGL_CLOSED",
    "CHRONOS_RR_PROVED",
    "CHRONOS_RR_CLOSED",
    "P_VS_NP_PROVED",
    "CLAY_PROBLEM_PROVED",
    "UNCONDITIONAL_THEOREM_CLOSURE",
)


def fail(message: str) -> None:
    raise SystemExit(f"R1A_TRIVIAL_TWO_FACE_BOUNDARY_STATEMENT_SURFACE_FAILED: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def flatten_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from flatten_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from flatten_strings(item)


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"could not read artifact: {exc}")


def main() -> None:
    artifact_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not artifact_path.is_absolute():
        artifact_path = ROOT / artifact_path

    data = load(artifact_path)

    require(data.get("artifact") == "R1A_TRIVIAL_TWO_FACE_BOUNDARY_STATEMENT_SURFACE", "wrong artifact")
    require(data.get("repository") == "chronos-urf-rr", "wrong repository")
    require(data.get("frontier_item") == "R1", "wrong frontier item")
    require(data.get("substep") == "R1a", "wrong substep")
    require(data.get("status") == "STATEMENT_SURFACE_ONLY_NO_THEOREM_CLOSURE", "wrong status")
    require(data.get("target") == "R1aTrivialTwoFaceBoundaryLongChordExclusion", "wrong target")

    exact = data.get("exact_statement")
    require(isinstance(exact, dict), "exact_statement must be object")
    missing_exact = REQUIRED_EXACT_STATEMENT_KEYS - set(exact)
    require(not missing_exact, f"exact_statement missing keys: {sorted(missing_exact)}")
    require(
        exact["name"] == "R1a trivial 2-face boundary long-chord exclusion",
        "wrong exact statement name",
    )
    require(exact["conclusion"] == "e_i notin supp(partial tau)", "wrong R1a conclusion")
    require("trivial 2-face tau" in exact["formal_surface"], "missing trivial 2-face scope")
    require("long-chord edge e_i" in exact["formal_surface"], "missing long-chord edge scope")
    require("e_i is not in supp(partial tau)" in exact["formal_surface"], "missing boundary exclusion")

    quantifiers = exact.get("quantifiers")
    hypotheses = exact.get("hypotheses")
    require(isinstance(quantifiers, list) and len(quantifiers) == 3, "quantifiers must be three-item list")
    require(isinstance(hypotheses, list) and len(hypotheses) >= 3, "hypotheses list too weak")
    for token in [
        "repository_native_admissible_finite_patch_fgl_instance I",
        "trivial_2_face tau in Phi_2^triv(I)",
        "i in {1,2}",
    ]:
        require(any(token in item for item in quantifiers), f"missing quantifier token: {token}")
    for token in [
        "TrivialTwoFace(I,tau)",
        "LongChordEdge(I,e_i)",
        "BoundarySupport(I,partial tau) is defined",
    ]:
        require(token in hypotheses, f"missing hypothesis token: {token}")

    missing_input = data.get("weakest_missing_input")
    require(isinstance(missing_input, dict), "weakest_missing_input must be object")
    require(
        missing_input.get("name") == "TrivialTwoFaceBoundaryLongChordAbsence",
        "wrong weakest missing input name",
    )
    logical_form = missing_input.get("logical_form")
    require(isinstance(logical_form, str), "weakest missing input logical_form must be string")
    for token in [
        "trivial 2-face tau in Phi_2^triv(I)",
        "LongChordEdge(I,e_i)",
        "e_i notin supp(partial tau)",
    ]:
        require(token in logical_form, f"weakest input missing token: {token}")

    excluded = missing_input.get("strictly_does_not_include")
    require(isinstance(excluded, list), "strictly_does_not_include must be list")
    for token in [
        "R1b linear-combination closure",
        "R1c maximal-separation exclusion",
        "combined R1 Long-Chord Exclusion Lemma",
        "R2 Diameter-Separation Filling Obstruction",
        "R3 Uniform Local-Type Capacity Lemma",
        "FGL theorem closure",
        "Chronos-RR theorem closure",
        "P vs NP",
        "any Clay problem",
    ]:
        require(token in excluded, f"missing exclusion token: {token}")

    combination = data.get("combination_boundary")
    require(isinstance(combination, dict), "combination_boundary must be object")
    require("R1a remains a statement surface" in combination.get("after_this_surface", ""), "missing R1a boundary")
    require("Linear combinations" in combination.get("r1b_required_after_r1a", ""), "missing R1b dependency")
    require("Maximal-separation" in combination.get("r1c_required_after_r1b", ""), "missing R1c dependency")
    require("R1a, R1b, and R1c" in combination.get("r1_combination_required", ""), "missing combined R1 dependency")

    boundary = data.get("boundary")
    require(isinstance(boundary, dict), "boundary must be object")
    require(boundary.get("evidence_class") == "statement_surface_only", "wrong evidence class")

    proof_claims = boundary.get("proof_claims")
    require(isinstance(proof_claims, dict), "proof_claims must be object")
    for key in FORBIDDEN_TRUE_CLAIMS:
        require(proof_claims.get(key) is False, f"overclaiming proof flag: {key}")

    non_claims = boundary.get("required_non_claims")
    require(isinstance(non_claims, list), "required_non_claims must be list")
    missing_non_claims = REQUIRED_NON_CLAIMS - set(non_claims)
    require(not missing_non_claims, f"missing non-claims: {sorted(missing_non_claims)}")

    for text in flatten_strings(data):
        for token in FORBIDDEN_OVERCLAIM_TOKENS:
            require(token not in text, f"forbidden overclaim token: {token}")

    print("R1A_TRIVIAL_TWO_FACE_BOUNDARY_STATEMENT_SURFACE_OK")


if __name__ == "__main__":
    main()
