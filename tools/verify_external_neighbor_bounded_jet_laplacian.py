#!/usr/bin/env python3
import json
import os
import sys

import numpy as np


OUTPUT_PATH = "artifacts/external_validation/external_neighbor_bounded_jet_laplacian_2026_06_29.json"


def external_neighbor_bounded_jet_laplacian_witness(
    num_nodes: int = 4,
    dimension: int = 3,
    jet_order: int = 2,
    projection_rank: int = 2,
    seed: int = 20260628,
    svd_tol: float = 1e-8,
) -> dict:
    if num_nodes <= 1:
        raise ValueError("num_nodes must be > 1")
    if dimension <= 0:
        raise ValueError("dimension must be positive")
    if jet_order < 0:
        raise ValueError("jet_order must be nonnegative")

    block_dim = dimension * (jet_order + 1)
    total_dim = num_nodes * block_dim

    if not (0 <= projection_rank <= block_dim):
        raise ValueError("projection_rank must lie in [0, block_dim]")

    rng = np.random.default_rng(seed)

    b_rigid = np.zeros((total_dim, total_dim), dtype=float)
    for i in range(num_nodes):
        start = i * block_dim
        end = start + block_dim
        q, _ = np.linalg.qr(rng.standard_normal((block_dim, block_dim)))
        diag = np.zeros(block_dim, dtype=float)
        diag[:projection_rank] = 1.0
        b_rigid[start:end, start:end] = q @ np.diag(diag) @ q.T

    a_jet = np.zeros((total_dim, total_dim), dtype=float)
    overlap_axis = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            decay = 1.0 / (i + j + 1.2)
            overlap_axis.append(
                {
                    "source": i,
                    "target": j,
                    "diagnostic_decay": decay,
                    "semantic_role": "finite_weight_only",
                }
            )
            ii = i * block_dim
            jj = j * block_dim
            a_jet[ii : ii + block_dim, jj : jj + block_dim] = np.eye(block_dim) * decay
            a_jet[jj : jj + block_dim, ii : ii + block_dim] = np.eye(block_dim) * decay

    d_spec = np.diag(np.sum(a_jet, axis=1))
    l_ux = d_spec - a_jet + b_rigid

    singular_values = np.linalg.svd(l_ux, compute_uv=False)
    sorted_singular_values = np.sort(singular_values)
    rank = int(np.sum(singular_values > svd_tol))
    nullity = int(total_dim - rank)

    return {
        "object": "external_neighbor_bounded_jet_laplacian_witness",
        "boundary_status": "finite_seeded_numeric_witness_only",
        "parameters": {
            "num_nodes": num_nodes,
            "dimension": dimension,
            "jet_order": jet_order,
            "projection_rank": projection_rank,
            "seed": seed,
            "svd_tol": svd_tol,
            "block_dim": block_dim,
            "operator_dim": total_dim,
        },
        "metrics": {
            "verified_rank": rank,
            "structural_nullity": nullity,
            "rank_plus_nullity": rank + nullity,
            "lowest_singular_values": [float(x) for x in sorted_singular_values[:6]],
            "lowest_positive_singular_values": [
                float(x) for x in sorted_singular_values if x > svd_tol
            ][:5],
        },
        "overlap_axis": overlap_axis,
        "locked_out_claims": [
            "no_continuous_metric_backreaction_claim",
            "no_einstein_field_limit_claim",
            "no_general_rank_stability_claim",
            "no_gravity_closure_claim",
            "no_universal_operator_theorem_claim",
        ],
    }


def enforce_strict_verifier_checks(artifact: dict) -> None:
    forbidden_keys = {
        "continuous_field_theorem",
        "gravity_closure",
        "einstein_limit_proof",
        "universal_rank_stability",
    }

    metrics = artifact.get("metrics", {})
    params = artifact.get("parameters", {})

    if metrics.get("structural_nullity") != 1:
        raise AssertionError("structural_nullity must equal 1 for this finite witness")
    if metrics.get("verified_rank") != 35:
        raise AssertionError("verified_rank must equal 35 for this finite witness")
    if metrics.get("rank_plus_nullity") != params.get("operator_dim"):
        raise AssertionError("rank_plus_nullity must equal operator_dim")

    artifact_keys = set(artifact)
    parameter_keys = set(params)
    detected = sorted((artifact_keys | parameter_keys) & forbidden_keys)
    if detected:
        raise AssertionError(f"prohibited claim keys detected: {detected}")

    locked = set(artifact.get("locked_out_claims", []))
    required_locks = {
        "no_continuous_metric_backreaction_claim",
        "no_einstein_field_limit_claim",
        "no_general_rank_stability_claim",
        "no_gravity_closure_claim",
        "no_universal_operator_theorem_claim",
    }
    missing = sorted(required_locks - locked)
    if missing:
        raise AssertionError(f"missing locked-out claims: {missing}")


def main() -> None:
    artifact = external_neighbor_bounded_jet_laplacian_witness()
    enforce_strict_verifier_checks(artifact)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(artifact, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("EXTERNAL_NEIGHBOR_BOUNDED_JET_LAPLACIAN_OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"EXTERNAL_NEIGHBOR_BOUNDED_JET_LAPLACIAN_FAIL: {exc}", file=sys.stderr)
        raise
