#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from itertools import combinations, product
from pathlib import Path
from typing import Any, Iterable

DEFAULT_PACKET = Path("artifacts/chronos/r2_cross_root_face_incidence_packet_2026_07_20.json")


def fail(message: str) -> None:
    raise SystemExit(f"R2_CROSS_ROOT_FACE_INCIDENCE_PACKET_ERROR: {message}")


def xor_vectors(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x ^ y for x, y in zip(a, b))


def mat_vec(matrix: list[list[int]], vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(x * y for x, y in zip(row, vector)) % 2 for row in matrix)


def mat_mul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    if not left or not right:
        return []
    columns = list(zip(*right))
    return [
        [sum(x * y for x, y in zip(row, column)) % 2 for column in columns]
        for row in left
    ]


def gf2_rank(matrix: list[list[int]]) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next((i for i in range(pivot_row, row_count) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        for i in range(row_count):
            if i != pivot_row and rows[i][column]:
                rows[i] = [x ^ y for x, y in zip(rows[i], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def all_vectors(dimension: int) -> Iterable[tuple[int, ...]]:
    return product((0, 1), repeat=dimension)


def image_vectors(matrix: list[list[int]], domain_dimension: int) -> set[tuple[int, ...]]:
    return {mat_vec(matrix, vector) for vector in all_vectors(domain_dimension)}


def quotient_classes(
    cycles: set[tuple[int, ...]], boundaries: set[tuple[int, ...]]
) -> list[set[tuple[int, ...]]]:
    remaining = set(cycles)
    classes: list[set[tuple[int, ...]]] = []
    while remaining:
        representative = min(remaining)
        equivalence_class = {
            xor_vectors(representative, boundary)
            for boundary in boundaries
            if xor_vectors(representative, boundary) in cycles
        }
        if not equivalence_class:
            fail("empty quotient equivalence class")
        classes.append(equivalence_class)
        remaining -= equivalence_class
    return classes


def connected_components(nodes: set[str], adjacency: dict[str, set[str]]) -> list[set[str]]:
    remaining = set(nodes)
    components: list[set[str]] = []
    while remaining:
        start = min(remaining)
        stack = [start]
        component: set[str] = set()
        while stack:
            node = stack.pop()
            if node in component:
                continue
            component.add(node)
            stack.extend(adjacency[node] & nodes)
        components.append(component)
        remaining -= component
    return components


def validate_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        fail(f"duplicate {label}")


def compute(packet: dict[str, Any]) -> dict[str, Any]:
    roots = packet["roots"]
    vertices = packet["vertices"]
    edge_entries = packet["edges"]
    face_entries = packet["faces"]
    rooted_regions = packet["rooted_regions"]

    validate_unique(roots, "roots")
    validate_unique(vertices, "vertices")

    edges = [entry["id"] for entry in edge_entries]
    faces = [entry["id"] for entry in face_entries]
    validate_unique(edges, "edge identifiers")
    validate_unique(faces, "face identifiers")

    vertex_set = set(vertices)
    edge_set = set(edges)
    face_set = set(faces)
    root_set = set(roots)

    endpoints: dict[str, tuple[str, str]] = {}
    for entry in edge_entries:
        edge = entry["id"]
        pair = tuple(entry["endpoints"])
        if len(pair) != 2 or pair[0] == pair[1] or not set(pair) <= vertex_set:
            fail(f"invalid endpoints for edge {edge}")
        endpoints[edge] = pair  # type: ignore[assignment]

    face_boundaries: dict[str, set[str]] = {}
    face_roots: dict[str, set[str]] = {}
    for entry in face_entries:
        face = entry["id"]
        boundary = set(entry["boundary"])
        incidences = set(entry["root_incidence"])
        if len(boundary) != 3 or not boundary <= edge_set:
            fail(f"face {face} must list exactly three existing boundary edges")
        if not incidences or not incidences <= root_set:
            fail(f"face {face} has invalid root incidence")
        endpoint_degrees = {vertex: 0 for vertex in vertices}
        for edge in boundary:
            for vertex in endpoints[edge]:
                endpoint_degrees[vertex] += 1
        used_degrees = sorted(degree for degree in endpoint_degrees.values() if degree)
        if used_degrees != [2, 2, 2]:
            fail(f"face {face} boundary is not a triangle")
        face_boundaries[face] = boundary
        face_roots[face] = incidences

    d1 = [[int(vertex in endpoints[edge]) for edge in edges] for vertex in vertices]
    d2 = [[int(edge in face_boundaries[face]) for face in faces] for edge in edges]
    d1d2 = mat_mul(d1, d2)
    d1_d2_zero = all(value == 0 for row in d1d2 for value in row)
    if not d1_d2_zero:
        fail("D1 D2 is nonzero")

    local_results: dict[str, Any] = {}
    nonzero_representatives: dict[str, list[tuple[int, ...]]] = {}
    for root in roots:
        if root not in rooted_regions:
            fail(f"missing rooted region {root}")
        region = rooted_regions[root]
        local_vertices = region["vertices"]
        local_edges = region["edges"]
        if not set(local_vertices) <= vertex_set or not set(local_edges) <= edge_set:
            fail(f"rooted region {root} references unknown objects")
        for edge in local_edges:
            if not set(endpoints[edge]) <= set(local_vertices):
                fail(f"rooted region {root} contains edge {edge} without both endpoints")

        local_faces = [
            face for face in faces if face_boundaries[face] <= set(local_edges)
        ]
        local_d1 = [
            [int(vertex in endpoints[edge]) for edge in local_edges]
            for vertex in local_vertices
        ]
        local_d2 = [
            [int(edge in face_boundaries[face]) for face in local_faces]
            for edge in local_edges
        ]
        cycles = {
            vector
            for vector in all_vectors(len(local_edges))
            if all(value == 0 for value in mat_vec(local_d1, vector))
        }
        boundaries = image_vectors(local_d2, len(local_faces))
        if not boundaries <= cycles:
            fail(f"local boundaries are not cycles at root {root}")
        classes = quotient_classes(cycles, boundaries)
        class_count = len(classes)
        quotient_dimension = int(math.log2(class_count)) if class_count else -1
        if class_count != 2**quotient_dimension:
            fail(f"root {root} quotient class count is not a power of two")
        zero = tuple(0 for _ in local_edges)
        nonzero_classes = [equivalence_class for equivalence_class in classes if zero not in equivalence_class]
        representatives = [min(equivalence_class) for equivalence_class in nonzero_classes]
        nonzero_representatives[root] = representatives
        local_results[root] = {
            "vertices": local_vertices,
            "edges": local_edges,
            "faces": local_faces,
            "d1_rank": gf2_rank(local_d1),
            "d2_rank": gf2_rank(local_d2),
            "cycle_count": len(cycles),
            "boundary_count": len(boundaries),
            "quotient_class_count": class_count,
            "quotient_dimension": quotient_dimension,
            "nonzero_class_representatives": [list(vector) for vector in representatives],
        }

    face_adjacency: dict[str, set[str]] = {face: set() for face in faces}
    for left, right in combinations(faces, 2):
        if face_boundaries[left] & face_boundaries[right]:
            face_adjacency[left].add(right)
            face_adjacency[right].add(left)

    systems: list[dict[str, Any]] = []
    for left_index, left_root in enumerate(roots):
        for right_root in roots[left_index + 1 :]:
            left_edges = rooted_regions[left_root]["edges"]
            right_edges = rooted_regions[right_root]["edges"]
            for left_rep in nonzero_representatives[left_root]:
                for right_rep in nonzero_representatives[right_root]:
                    rhs = [0] * len(edges)
                    for bit, edge in zip(left_rep, left_edges):
                        rhs[edges.index(edge)] ^= bit
                    for bit, edge in zip(right_rep, right_edges):
                        rhs[edges.index(edge)] ^= bit
                    rhs_tuple = tuple(rhs)
                    solutions = [
                        vector
                        for vector in all_vectors(len(faces))
                        if mat_vec(d2, vector) == rhs_tuple
                    ]
                    solution_records: list[dict[str, Any]] = []
                    for solution in solutions:
                        support = {face for bit, face in zip(solution, faces) if bit}
                        components = connected_components(support, face_adjacency)
                        component_records = []
                        for component in components:
                            incident_roots = sorted(
                                set().union(*(face_roots[face] for face in component))
                            )
                            component_records.append(
                                {
                                    "faces": sorted(component),
                                    "incident_roots": incident_roots,
                                }
                            )
                        has_cross_root_component = any(
                            len(record["incident_roots"]) >= 2 for record in component_records
                        )
                        solution_records.append(
                            {
                                "face_vector": list(solution),
                                "support": sorted(support),
                                "components": component_records,
                                "has_cross_root_component": has_cross_root_component,
                            }
                        )
                    systems.append(
                        {
                            "roots": [left_root, right_root],
                            "left_representative": list(left_rep),
                            "right_representative": list(right_rep),
                            "rhs": list(rhs_tuple),
                            "solutions": solution_records,
                        }
                    )

    solvable_systems = [system for system in systems if system["solutions"]]
    replacement_theorem_holds = all(
        solution["has_cross_root_component"]
        for system in solvable_systems
        for solution in system["solutions"]
    )
    nonvacuous = (
        len(roots) >= 2
        and all(nonzero_representatives[root] for root in roots)
        and bool(solvable_systems)
    )
    if not nonvacuous:
        fail("packet is vacuous")
    if not replacement_theorem_holds:
        fail("cross-root face-incidence replacement theorem fails")

    result = {
        "d1": d1,
        "d2": d2,
        "d1_d2": d1d2,
        "d1_d2_zero": d1_d2_zero,
        "local_results": local_results,
        "cross_root_systems": systems,
        "cross_root_system_count": len(systems),
        "solvable_cross_root_system_count": len(solvable_systems),
        "replacement_theorem_holds": replacement_theorem_holds,
        "nonvacuous": nonvacuous,
    }
    return result


def verify_expected(packet: dict[str, Any], result: dict[str, Any]) -> None:
    expected = packet["expected_certificate"]
    actual_dimensions = {
        root: data["quotient_dimension"] for root, data in result["local_results"].items()
    }
    checks = {
        "d1_d2_zero": result["d1_d2_zero"],
        "local_quotient_dimensions": actual_dimensions,
        "cross_root_system_count": result["cross_root_system_count"],
        "solvable_cross_root_system_count": result["solvable_cross_root_system_count"],
        "replacement_theorem_holds": result["replacement_theorem_holds"],
    }
    if checks != expected:
        fail(f"computed certificate mismatch: expected {expected!r}, got {checks!r}")


def main() -> None:
    packet_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    packet = json.loads(packet_path.read_text())
    result = compute(packet)
    verify_expected(packet, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    print("R2_CROSS_ROOT_FACE_INCIDENCE_PACKET_OK")


if __name__ == "__main__":
    main()
