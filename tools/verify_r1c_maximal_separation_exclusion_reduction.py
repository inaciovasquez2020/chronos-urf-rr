#!/usr/bin/env python3

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "artifacts/chronos/r1c_maximal_separation_exclusion_reduction_2026_06_15.json"

REQUIRED_NON_CLAIMS = {
    "does not prove R1a",
    "does not prove full R1b",
    "does not prove R1c without the diameter inputs",
    "does not prove combined R1 Long-Chord Exclusion Lemma",
    "does not prove FGL",
    "does not prove Chronos-RR",
    "does not prove P vs NP",
    "does not prove any Clay problem",
}

FORBIDDEN_TRUE_CLAIMS = {
    "proves_r1a",
    "proves_r1b_full",
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
    "R1B_FULL_PROVED",
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
    raise SystemExit(f"R1C_MAXIMAL_SEPARATION_EXCLUSION_REDUCTION_FAILED: {message}")


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


def contradiction_from_bounds(long_chord_separation: int, local_patch_bound: int) -> bool:
    require(long_chord_separation >= 0, "separation must be nonnegative")
    require(local_patch_bound >= 0, "local patch bound must be nonnegative")
    if not local_patch_bound < long_chord_separation:
        return False
    # If the edge is present, the support diameter must be at least the endpoint separation.
    # If the support is locally bounded, the support diameter must be at most local_patch_bound.
    # Both can hold only if long_chord_separation <= local_patch_bound, contradicting the strict bound.
    return not (long_chord_separation <= local_patch_bound)


def check_strict_order_contradiction() -> None:
    positive_examples = [(1, 0), (2, 1), (10, 3), (99, 98)]
    for separation, bound in positive_examples:
        require(
            contradiction_from_bounds(separation, bound),
            f"expected contradiction for separation={separation}, bound={bound}",
        )

    negative_examples = [(0, 0), (1, 1), (2, 3), (5, 5)]
    for separation, bound in negative_examples:
        require(
            not contradiction_from_bounds(separation, bound),
            f"unexpected contradiction for separation={separation}, bound={bound}",
        )


def main() -> None:
    artifact_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not artifact_path.is_absolute():
        artifact_path = ROOT / artifact_path

    data = load(artifact_path)

    require(data.get("artifact") == "R1C_MAXIMAL_SEPARATION_EXCLUSION_REDUCTION", "wrong artifact")
    require(data.get("repository") == "chronos-urf-rr", "wrong repository")
    require(data.get("frontier_item") == "R1", "wrong frontier item")
    require(data.get("substep") == "R1c", "wrong substep")
    require(
        data.get("status") == "GEOMETRIC_REDUCTION_PROVED_CONDITIONAL_ON_MAXIMAL_SEPARATION_DIAMETER_BOUND",
        "wrong status",
    )
    require(data.get("target") == "R1cMaximalSeparationLongChordExclusion", "wrong target")

    exact = data.get("exact_statement")
    require(isinstance(exact, dict), "exact_statement must be object")
    require(exact.get("conclusion") == "e_i notin supp(w)", "wrong R1c conclusion")
    require("strictly less than D_i" in exact.get("formal_surface", ""), "missing strict diameter bound")
    require("diameter at least D_i" in exact.get("geometric_core", ""), "missing support lower bound")
    require("local patch" in exact.get("geometric_core", ""), "missing local-patch upper bound")

    quantifiers = exact.get("quantifiers")
    hypotheses = exact.get("hypotheses")
    require(isinstance(quantifiers, list) and len(quantifiers) == 3, "quantifiers must be three-item list")
    require(isinstance(hypotheses, list), "hypotheses must be list")
    for token in [
        "LongChordEdge(I,e_i)",
        "MaximalEndpointSeparation(I,e_i,D_i)",
        "TrivialWitnessBoundary(I,w)",
        "LocalPatchDiameterBound(I,w) < D_i",
    ]:
        require(token in hypotheses, f"missing hypothesis: {token}")

    proof = data.get("proof_certificate")
    require(isinstance(proof, dict), "proof_certificate must be object")
    require(proof.get("order_type") == "strict_diameter_inequality", "wrong order type")
    require(proof.get("machine_checked_strict_order_contradiction") is True, "strict-order flag must be true")
    require(proof.get("contradiction") == "D_i <= delta_w and delta_w < D_i", "wrong contradiction")
    derivation = proof.get("derivation")
    require(isinstance(derivation, list) and len(derivation) == 6, "derivation must have six steps")
    require("D_i <= delta_w < D_i" in " ".join(derivation), "missing contradiction chain")

    discharged = data.get("discharged_subclaim")
    require(isinstance(discharged, dict), "discharged_subclaim must be object")
    require(discharged.get("discharged") is True, "geometric reduction must be marked discharged")
    require(
        discharged.get("name") == "R1c geometric exclusion from maximal-separation diameter bound",
        "wrong discharged subclaim name",
    )
    conditionals = set(discharged.get("conditional_on", []))
    require(
        "repository-native support-diameter bridge: containing e_i forces support diameter at least EndpointSeparation(e_i)" in conditionals,
        "missing support-diameter bridge conditional",
    )
    require(
        "repository-native local-patch containment: trivial witness boundary support diameter is bounded by its local patch diameter" in conditionals,
        "missing local-patch containment conditional",
    )
    require(
        "repository-native maximal-separation estimate: local patch diameter bound is strictly less than each long-chord endpoint separation" in conditionals,
        "missing maximal-separation estimate conditional",
    )

    remaining = data.get("remaining_for_r1")
    require(isinstance(remaining, dict), "remaining_for_r1 must be object")
    require("OPEN" in remaining.get("r1a", ""), "R1a must remain open")
    require("CONDITIONAL" in remaining.get("r1b", ""), "R1b boundary must remain conditional")
    require("OPEN" in remaining.get("r1c_inputs", ""), "R1c inputs must remain open")
    require("generation" in remaining.get("generation_bridge", "").lower(), "missing generation bridge boundary")

    boundary = data.get("boundary")
    require(isinstance(boundary, dict), "boundary must be object")
    require(boundary.get("evidence_class") == "geometric_reduction_certificate_only", "wrong evidence class")
    claims = boundary.get("proof_claims")
    require(isinstance(claims, dict), "proof_claims must be object")
    require(
        claims.get("proves_r1c_geometric_reduction_from_diameter_bound") is True,
        "must claim only the R1c geometric reduction from diameter bound",
    )
    for claim in FORBIDDEN_TRUE_CLAIMS:
        require(claim in claims, f"missing proof flag: {claim}")
        require(claims[claim] is False, f"overclaiming proof flag: {claim}")

    non_claims = set(boundary.get("required_non_claims", []))
    missing_non_claims = REQUIRED_NON_CLAIMS - non_claims
    require(not missing_non_claims, f"missing non-claims: {sorted(missing_non_claims)}")

    all_text = "\n".join(flatten_strings(data))
    for token in FORBIDDEN_OVERCLAIM_TOKENS:
        require(token not in all_text, f"forbidden overclaim token: {token}")

    check_strict_order_contradiction()

    print("R1C_MAXIMAL_SEPARATION_EXCLUSION_REDUCTION_OK")


if __name__ == "__main__":
    main()
