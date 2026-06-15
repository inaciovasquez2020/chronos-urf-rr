#!/usr/bin/env python3

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "artifacts/chronos/r1b_f2_linear_combination_no_new_long_chord_reduction_2026_06_15.json"

REQUIRED_NON_CLAIMS = {
    "does not prove R1a",
    "does not prove R1c",
    "does not prove combined R1 Long-Chord Exclusion Lemma",
    "does not prove FGL",
    "does not prove Chronos-RR",
    "does not prove P vs NP",
    "does not prove any Clay problem",
}

FORBIDDEN_TRUE_CLAIMS = {
    "proves_r1a",
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
    "R1C_PROVED",
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
    raise SystemExit(f"R1B_F2_LINEAR_COMBINATION_REDUCTION_FAILED: {message}")


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


def f2_sum_coordinate(coefficients, generator_edge_bits) -> int:
    total = 0
    for coeff, bit in zip(coefficients, generator_edge_bits):
        require(coeff in (0, 1), f"coefficient outside F2: {coeff}")
        require(bit in (0, 1), f"generator edge bit outside F2: {bit}")
        total ^= coeff & bit
    return total


def check_boolean_identity(max_generators: int = 8) -> None:
    for n in range(max_generators + 1):
        zero_generator_bits = [0] * n
        for coefficients in itertools.product((0, 1), repeat=n):
            result = f2_sum_coordinate(coefficients, zero_generator_bits)
            require(result == 0, f"F2 zero-generator identity failed at n={n}")

    # Negative sanity check: the verifier must distinguish absence from presence.
    require(f2_sum_coordinate([1], [1]) == 1, "negative sanity check failed")
    require(f2_sum_coordinate([1, 1], [1, 1]) == 0, "F2 cancellation sanity check failed")
    require(f2_sum_coordinate([1, 0, 1], [1, 1, 0]) == 1, "mixed-coordinate sanity check failed")


def main() -> None:
    artifact_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not artifact_path.is_absolute():
        artifact_path = ROOT / artifact_path

    data = load(artifact_path)

    require(
        data.get("artifact") == "R1B_F2_LINEAR_COMBINATION_NO_NEW_LONG_CHORD_REDUCTION",
        "wrong artifact",
    )
    require(data.get("repository") == "chronos-urf-rr", "wrong repository")
    require(data.get("frontier_item") == "R1", "wrong frontier item")
    require(data.get("substep") == "R1b", "wrong substep")
    require(
        data.get("status") == "ALGEBRAIC_REDUCTION_PROVED_CONDITIONAL_ON_R1A_GENERATOR_ABSENCE",
        "wrong status",
    )
    require(data.get("target") == "R1bF2LinearCombinationNoNewLongChord", "wrong target")

    exact = data.get("exact_statement")
    require(isinstance(exact, dict), "exact_statement must be object")
    require(exact.get("conclusion") == "e_i notin supp(sum_j a_j b_j)", "wrong R1b conclusion")
    require("xor_j" in exact.get("algebraic_core", ""), "missing xor algebraic core")
    require("generator-level absence" in exact.get("r1_dependency_role", ""), "missing R1a dependency")

    proof = data.get("proof_certificate")
    require(isinstance(proof, dict), "proof_certificate must be object")
    require(proof.get("field") == "F2", "wrong proof field")
    require(proof.get("machine_checked_boolean_identity") is True, "boolean identity flag must be true")
    require(
        proof.get("sum_coordinate_rule")
        == "indicator(e_i in supp(sum_j a_j b_j)) = xor_j (a_j AND indicator(e_i in supp(b_j)))",
        "wrong coordinate rule",
    )
    derivation = proof.get("derivation")
    require(isinstance(derivation, list) and len(derivation) == 5, "derivation must have five steps")
    require("xor of a finite family of zeros is 0" in " ".join(derivation), "missing zero-xor step")

    discharged = data.get("discharged_subclaim")
    require(isinstance(discharged, dict), "discharged_subclaim must be object")
    require(discharged.get("discharged") is True, "R1b algebraic reduction must be marked discharged")
    require(
        discharged.get("name") == "R1b algebraic closure from R1a generator absence",
        "wrong discharged subclaim name",
    )
    conditionals = set(discharged.get("conditional_on", []))
    require(
        "R1a generator-level absence for each trivial 2-face boundary" in conditionals,
        "missing R1a conditional",
    )
    require(
        "repository-native definition that W^triv is generated over F2 by trivial 2-face boundaries" in conditionals,
        "missing generation-bridge conditional",
    )

    remaining = data.get("remaining_for_r1")
    require(isinstance(remaining, dict), "remaining_for_r1 must be object")
    require("OPEN" in remaining.get("r1a", ""), "R1a must remain open")
    require("OPEN" in remaining.get("r1c", ""), "R1c must remain open")
    require("generation" in remaining.get("generation_bridge", "").lower(), "missing generation bridge boundary")

    boundary = data.get("boundary")
    require(isinstance(boundary, dict), "boundary must be object")
    require(boundary.get("evidence_class") == "algebraic_reduction_certificate_only", "wrong evidence class")
    claims = boundary.get("proof_claims")
    require(isinstance(claims, dict), "proof_claims must be object")
    require(
        claims.get("proves_r1b_algebraic_reduction_from_r1a") is True,
        "must claim only the R1b algebraic reduction from R1a",
    )
    for key in FORBIDDEN_TRUE_CLAIMS:
        require(claims.get(key) is False, f"overclaiming proof flag: {key}")

    non_claims = set(boundary.get("required_non_claims", []))
    missing_non_claims = REQUIRED_NON_CLAIMS - non_claims
    require(not missing_non_claims, f"missing non-claims: {sorted(missing_non_claims)}")

    all_text = "\n".join(flatten_strings(data))
    for token in FORBIDDEN_OVERCLAIM_TOKENS:
        require(token not in all_text, f"forbidden overclaim token: {token}")

    check_boolean_identity()
    print("R1B_F2_LINEAR_COMBINATION_REDUCTION_OK")


if __name__ == "__main__":
    main()
