#!/usr/bin/env python3
"""Verify closest external-neighbor boundary artifact.

This verifier is intentionally narrow: it checks only that the closest
external-neighbor artifact preserves the required non-claim boundary,
including no_gravity_closure for every listed neighbor.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ARTIFACT = Path("artifacts/external_validation/closest_external_neighbors_2026_06_28.json")

REQUIRED_TOP_LEVEL_FIELDS = {
    "nearest_neighbors",
    "overlap_axis",
    "distance_axis",
    "non_claim_boundary",
}

ALLOWED_BOUNDARIES = {
    "no_gravity_closure",
    "not_einstein_limit",
    "not_green_kernel_estimate_proof",
    "not_physical_metric_backreaction_law",
    "not_experimental_validation",
    "not_external_problem_closure",
    "not_physical_field_equation",
}

REQUIRED_GLOBAL_BOUNDARIES = {
    "no_gravity_closure",
    "not_einstein_limit",
    "not_experimental_validation",
    "not_external_problem_closure",
}


def fail(message: str) -> None:
    print(f"CLOSEST_EXTERNAL_NEIGHBORS_VERIFY_FAIL: {message}")
    raise SystemExit(1)


def require_list(data: dict[str, Any], field: str) -> list[Any]:
    value = data.get(field)
    if not isinstance(value, list) or not value:
        fail(f"{field} must be a nonempty list")
    return value


def require_string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        fail(f"{field} must be a nonempty list")
    if not all(isinstance(item, str) and item for item in value):
        fail(f"{field} must contain only nonempty strings")
    return value


def main() -> None:
    if not ARTIFACT.exists():
        fail(f"missing artifact: {ARTIFACT}")

    try:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")

    if not isinstance(data, dict):
        fail("artifact root must be an object")

    missing = sorted(REQUIRED_TOP_LEVEL_FIELDS - set(data))
    if missing:
        fail(f"missing top-level fields: {missing}")

    global_boundaries = set(require_string_list(data["non_claim_boundary"], "non_claim_boundary"))
    unknown_global = sorted(global_boundaries - ALLOWED_BOUNDARIES)
    if unknown_global:
        fail(f"unknown global boundaries: {unknown_global}")

    missing_global = sorted(REQUIRED_GLOBAL_BOUNDARIES - global_boundaries)
    if missing_global:
        fail(f"missing required global boundaries: {missing_global}")

    require_string_list(data["overlap_axis"], "overlap_axis")
    require_string_list(data["distance_axis"], "distance_axis")

    neighbors = require_list(data, "nearest_neighbors")
    ranks: set[int] = set()

    for index, neighbor in enumerate(neighbors):
        if not isinstance(neighbor, dict):
            fail(f"nearest_neighbors[{index}] must be an object")

        for field in ("rank", "name", "overlap_axis", "distance_axis", "non_claim_boundary"):
            if field not in neighbor:
                fail(f"nearest_neighbors[{index}] missing field: {field}")

        rank = neighbor["rank"]
        if not isinstance(rank, int) or rank <= 0:
            fail(f"nearest_neighbors[{index}].rank must be a positive integer")
        if rank in ranks:
            fail(f"duplicate neighbor rank: {rank}")
        ranks.add(rank)

        if not isinstance(neighbor["name"], str) or not neighbor["name"]:
            fail(f"nearest_neighbors[{index}].name must be a nonempty string")

        require_string_list(neighbor["overlap_axis"], f"nearest_neighbors[{index}].overlap_axis")
        require_string_list(neighbor["distance_axis"], f"nearest_neighbors[{index}].distance_axis")

        neighbor_boundaries = set(
            require_string_list(
                neighbor["non_claim_boundary"],
                f"nearest_neighbors[{index}].non_claim_boundary",
            )
        )

        unknown_neighbor = sorted(neighbor_boundaries - ALLOWED_BOUNDARIES)
        if unknown_neighbor:
            fail(f"nearest_neighbors[{index}] has unknown boundaries: {unknown_neighbor}")

        if "no_gravity_closure" not in neighbor_boundaries:
            fail(f"nearest_neighbors[{index}] does not preserve no_gravity_closure")

    print("CLOSEST_EXTERNAL_NEIGHBORS_VERIFY_OK")


if __name__ == "__main__":
    main()
