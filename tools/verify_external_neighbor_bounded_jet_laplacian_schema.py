#!/usr/bin/env python3
import json
import sys
from pathlib import Path


ARTIFACT_PATH = Path(
    "artifacts/external_validation/external_neighbor_bounded_jet_laplacian_2026_06_29.json"
)

EXPECTED_TOP_LEVEL_KEYS = {
    "boundary_status",
    "locked_out_claims",
    "metrics",
    "object",
    "overlap_axis",
    "parameters",
}

EXPECTED_PARAMETER_KEYS = {
    "block_dim",
    "dimension",
    "jet_order",
    "num_nodes",
    "operator_dim",
    "projection_rank",
    "seed",
    "svd_tol",
}

EXPECTED_METRIC_KEYS = {
    "lowest_positive_singular_values",
    "lowest_singular_values",
    "rank_plus_nullity",
    "structural_nullity",
    "verified_rank",
}

REQUIRED_LOCKS = {
    "no_continuous_metric_backreaction_claim",
    "no_einstein_field_limit_claim",
    "no_general_rank_stability_claim",
    "no_gravity_closure_claim",
    "no_universal_operator_theorem_claim",
}

FORBIDDEN_KEYS = {
    "continuous_field_theorem",
    "gravity_closure",
    "einstein_limit_proof",
    "universal_rank_stability",
    "metric_backreaction_law",
    "curvature_closure",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_exact_keys(name: str, value: dict, expected: set[str]) -> None:
    actual = set(value)
    require(
        actual == expected,
        f"{name} keys mismatch: expected {sorted(expected)}, got {sorted(actual)}",
    )


def require_int(name: str, value: object, expected: int | None = None) -> None:
    require(type(value) is int, f"{name} must be int")
    if expected is not None:
        require(value == expected, f"{name} must equal {expected}, got {value}")


def require_numeric(name: str, value: object) -> None:
    require(type(value) in {float, int}, f"{name} must be numeric")


def main() -> None:
    with ARTIFACT_PATH.open("r", encoding="utf-8") as handle:
        artifact = json.load(handle)

    require(type(artifact) is dict, "artifact must be an object")
    require_exact_keys("artifact", artifact, EXPECTED_TOP_LEVEL_KEYS)

    forbidden_detected = sorted(set(artifact) & FORBIDDEN_KEYS)
    require(not forbidden_detected, f"forbidden top-level keys detected: {forbidden_detected}")

    require(
        artifact["object"] == "external_neighbor_bounded_jet_laplacian_witness",
        "object name mismatch",
    )
    require(
        artifact["boundary_status"] == "finite_seeded_numeric_witness_only",
        "boundary_status mismatch",
    )

    parameters = artifact["parameters"]
    metrics = artifact["metrics"]
    locks = artifact["locked_out_claims"]
    overlap_axis = artifact["overlap_axis"]

    require(type(parameters) is dict, "parameters must be an object")
    require(type(metrics) is dict, "metrics must be an object")
    require(type(locks) is list, "locked_out_claims must be a list")
    require(type(overlap_axis) is list, "overlap_axis must be a list")

    require_exact_keys("parameters", parameters, EXPECTED_PARAMETER_KEYS)
    require_exact_keys("metrics", metrics, EXPECTED_METRIC_KEYS)

    forbidden_parameter_keys = sorted(set(parameters) & FORBIDDEN_KEYS)
    require(
        not forbidden_parameter_keys,
        f"forbidden parameter keys detected: {forbidden_parameter_keys}",
    )

    require_int("parameters.num_nodes", parameters["num_nodes"], 4)
    require_int("parameters.dimension", parameters["dimension"], 3)
    require_int("parameters.jet_order", parameters["jet_order"], 2)
    require_int("parameters.projection_rank", parameters["projection_rank"], 2)
    require_int("parameters.block_dim", parameters["block_dim"], 9)
    require_int("parameters.operator_dim", parameters["operator_dim"], 36)
    require_int("parameters.seed", parameters["seed"], 20260628)
    require_numeric("parameters.svd_tol", parameters["svd_tol"])
    require(parameters["svd_tol"] == 1e-8, "parameters.svd_tol must equal 1e-8")

    require_int("metrics.verified_rank", metrics["verified_rank"], 35)
    require_int("metrics.structural_nullity", metrics["structural_nullity"], 1)
    require_int("metrics.rank_plus_nullity", metrics["rank_plus_nullity"], 36)

    require(
        type(metrics["lowest_singular_values"]) is list
        and len(metrics["lowest_singular_values"]) == 6,
        "lowest_singular_values must contain exactly 6 entries",
    )
    require(
        type(metrics["lowest_positive_singular_values"]) is list
        and len(metrics["lowest_positive_singular_values"]) == 5,
        "lowest_positive_singular_values must contain exactly 5 entries",
    )

    for index, value in enumerate(metrics["lowest_singular_values"]):
        require_numeric(f"lowest_singular_values[{index}]", value)

    for index, value in enumerate(metrics["lowest_positive_singular_values"]):
        require_numeric(f"lowest_positive_singular_values[{index}]", value)
        require(
            value > parameters["svd_tol"],
            f"lowest_positive_singular_values[{index}] must exceed svd_tol",
        )

    require(set(locks) == REQUIRED_LOCKS, "locked_out_claims mismatch")
    require(len(overlap_axis) == 6, "overlap_axis must contain one entry for each unordered pair of 4 nodes")

    seen_pairs = set()
    for index, entry in enumerate(overlap_axis):
        require(type(entry) is dict, f"overlap_axis[{index}] must be an object")
        require(
            set(entry) == {"diagnostic_decay", "semantic_role", "source", "target"},
            f"overlap_axis[{index}] keys mismatch",
        )
        require_int(f"overlap_axis[{index}].source", entry["source"])
        require_int(f"overlap_axis[{index}].target", entry["target"])
        require(
            entry["source"] < entry["target"],
            f"overlap_axis[{index}] must be ordered source < target",
        )
        require_numeric(f"overlap_axis[{index}].diagnostic_decay", entry["diagnostic_decay"])
        require(
            entry["semantic_role"] == "finite_weight_only",
            f"overlap_axis[{index}].semantic_role must be finite_weight_only",
        )
        seen_pairs.add((entry["source"], entry["target"]))

    require(
        seen_pairs == {(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)},
        f"overlap_axis pair set mismatch: {sorted(seen_pairs)}",
    )

    print("EXTERNAL_NEIGHBOR_BOUNDED_JET_LAPLACIAN_SCHEMA_OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"EXTERNAL_NEIGHBOR_BOUNDED_JET_LAPLACIAN_SCHEMA_FAIL: {exc}", file=sys.stderr)
        raise
