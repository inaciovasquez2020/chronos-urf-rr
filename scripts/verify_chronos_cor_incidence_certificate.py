from __future__ import annotations
import json
from collections import deque
from pathlib import Path
from typing import Any

DEFAULT_CERT = Path("artifacts/cor/cor_incidence_basis_certificate_example.json")

REQUIRED_BOUNDARY = [
    "This finite incidence-basis certificate verifies raw GF(2) boundary annihilation.",
    "It verifies the finite cycle-space dimension from the incidence matrix.",
    "It verifies the finite local-cycle rank from radius-R graph balls.",
    "It does not prove the finite-to-general lift.",
    "It does not prove the locality-to-depth bridge.",
    "It does not prove theorem-level Chronos closure.",
]

FORBIDDEN = [
    "Chronos is solved",
    "theorem-level Chronos closure is proved",
    "unconditional Chronos closure",
    "finite-to-general lift is proved",
    "locality-to-depth bridge is proved",
    "P vs NP is solved",
]


def require_int(obj: dict[str, Any], key: str) -> int:
    value = obj.get(key)
    if not isinstance(value, int):
        raise SystemExit(f"{key} must be an integer")
    if value < 0:
        raise SystemExit(f"{key} must be nonnegative")
    return value


def normalize_vector(v: Any, width: int, name: str) -> list[int]:
    if not isinstance(v, list) or len(v) != width:
        raise SystemExit(f"{name} must be a list of length {width}")
    out = []
    for x in v:
        if x not in (0, 1):
            raise SystemExit(f"{name} entries must be 0 or 1")
        out.append(int(x))
    return out


def rank_gf2(vectors: list[list[int]], width: int) -> int:
    rows = [row[:] for row in vectors if any(row)]
    rank = 0
    for col in range(width):
        pivot = None
        for r in range(rank, len(rows)):
            if rows[r][col]:
                pivot = r
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][col]:
                rows[r] = [a ^ b for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def rref_gf2(rows: list[list[int]], width: int) -> tuple[list[list[int]], list[int]]:
    mat = [row[:] for row in rows]
    pivot_cols: list[int] = []
    rank = 0
    for col in range(width):
        pivot = None
        for r in range(rank, len(mat)):
            if mat[r][col]:
                pivot = r
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        for r in range(len(mat)):
            if r != rank and mat[r][col]:
                mat[r] = [a ^ b for a, b in zip(mat[r], mat[rank])]
        pivot_cols.append(col)
        rank += 1
    return mat[:rank], pivot_cols


def nullspace_basis_gf2(rows: list[list[int]], width: int) -> list[list[int]]:
    rref, pivots = rref_gf2(rows, width)
    pivot_set = set(pivots)
    free_cols = [c for c in range(width) if c not in pivot_set]
    basis: list[list[int]] = []
    for free in free_cols:
        x = [0] * width
        x[free] = 1
        for i, pivot in enumerate(pivots):
            x[pivot] = rref[i][free]
        basis.append(x)
    return basis


def boundary_matrix(vertex_count: int, edges: list[list[int]]) -> list[list[int]]:
    rows = [[0] * len(edges) for _ in range(vertex_count)]
    for j, (u, v) in enumerate(edges):
        rows[u][j] ^= 1
        rows[v][j] ^= 1
    return rows


def boundary_zero(vec: list[int], vertex_count: int, edges: list[list[int]]) -> bool:
    out = [0] * vertex_count
    for bit, (u, v) in zip(vec, edges):
        if bit:
            out[u] ^= 1
            out[v] ^= 1
    return not any(out)


def adjacency(vertex_count: int, edges: list[list[int]]) -> list[list[int]]:
    adj = [[] for _ in range(vertex_count)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def distances_from(center: int, adj: list[list[int]]) -> list[int | None]:
    dist: list[int | None] = [None] * len(adj)
    dist[center] = 0
    q: deque[int] = deque([center])
    while q:
        u = q.popleft()
        assert dist[u] is not None
        for v in adj[u]:
            if dist[v] is None:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def ball_edge_indices(center: int, radius: int, adj: list[list[int]], edges: list[list[int]]) -> list[int]:
    dist = distances_from(center, adj)
    indices = []
    for i, (u, v) in enumerate(edges):
        if dist[u] is not None and dist[v] is not None and dist[u] <= radius and dist[v] <= radius:
            indices.append(i)
    return indices


def local_cycle_generators(vertex_count: int, edges: list[list[int]], radius: int) -> list[list[int]]:
    adj = adjacency(vertex_count, edges)
    generators: list[list[int]] = []
    for center in range(vertex_count):
        idx = ball_edge_indices(center, radius, adj, edges)
        if not idx:
            continue
        local_edges = [edges[i] for i in idx]
        local_boundary = boundary_matrix(vertex_count, local_edges)
        for local_vec in nullspace_basis_gf2(local_boundary, len(local_edges)):
            full = [0] * len(edges)
            for bit, edge_idx in zip(local_vec, idx):
                full[edge_idx] = bit
            if any(full):
                generators.append(full)
    return generators


def verify_certificate(path: Path) -> None:
    raw = path.read_text()
    cert = json.loads(raw)

    if cert.get("certificate_type") != "chronos_cor_incidence_basis_certificate":
        raise SystemExit("wrong certificate_type")
    if cert.get("field") != "F2":
        raise SystemExit("field must be F2")

    radius = require_int(cert, "radius")
    vertex_count = require_int(cert, "vertex_count")
    if vertex_count == 0:
        raise SystemExit("vertex_count must be positive")

    edges_raw = cert.get("edges")
    if not isinstance(edges_raw, list) or not edges_raw:
        raise SystemExit("edges must be a nonempty list")

    edges: list[list[int]] = []
    for e in edges_raw:
        if (
            not isinstance(e, list)
            or len(e) != 2
            or not all(isinstance(x, int) for x in e)
        ):
            raise SystemExit("each edge must be [u, v]")
        u, v = e
        if u == v:
            raise SystemExit("loops are not allowed")
        if not (0 <= u < vertex_count and 0 <= v < vertex_count):
            raise SystemExit("edge endpoint outside vertex range")
        edges.append([u, v])

    edge_count = len(edges)

    cycle_basis = [
        normalize_vector(v, edge_count, "cycle_basis vector")
        for v in cert.get("cycle_basis", [])
    ]
    local_cycle_basis = [
        normalize_vector(v, edge_count, "local_cycle_basis vector")
        for v in cert.get("local_cycle_basis", [])
    ]

    bmat = boundary_matrix(vertex_count, edges)
    boundary_rank = rank_gf2(bmat, edge_count)
    computed_cycle_dim = edge_count - boundary_rank

    if computed_cycle_dim != require_int(cert, "cycle_space_dimension"):
        raise SystemExit("cycle_space_dimension does not match incidence nullity")

    if rank_gf2(cycle_basis, edge_count) != computed_cycle_dim:
        raise SystemExit("cycle_basis rank does not equal computed cycle-space dimension")
    for vec in cycle_basis:
        if not boundary_zero(vec, vertex_count, edges):
            raise SystemExit("cycle_basis vector is not in ker(boundary)")

    local_generators = local_cycle_generators(vertex_count, edges, radius)
    computed_local_rank = rank_gf2(local_generators, edge_count)
    declared_local_rank = require_int(cert, "local_cycle_subspace_rank")

    if computed_local_rank != declared_local_rank:
        raise SystemExit("local_cycle_subspace_rank does not match radius-R ball computation")
    if rank_gf2(local_cycle_basis, edge_count) != declared_local_rank:
        raise SystemExit("local_cycle_basis rank does not equal computed local rank")
    for vec in local_cycle_basis:
        if not boundary_zero(vec, vertex_count, edges):
            raise SystemExit("local_cycle_basis vector is not in ker(boundary)")
    if rank_gf2(local_generators + local_cycle_basis, edge_count) != computed_local_rank:
        raise SystemExit("local_cycle_basis is not contained in computed local span")

    cor = require_int(cert, "certified_obstruction_rank")
    if cor != computed_cycle_dim - computed_local_rank:
        raise SystemExit("certified_obstruction_rank must equal cycle_dim - local_rank")

    growth = cert.get("linear_growth_claim", {})
    if growth.get("enabled") is True:
        alpha_num = require_int(growth, "alpha_num")
        alpha_den = require_int(growth, "alpha_den")
        if alpha_num == 0 or alpha_den == 0:
            raise SystemExit("enabled alpha must be positive")
        if cor * alpha_den < alpha_num * vertex_count:
            raise SystemExit("linear growth inequality failed")

    boundary = cert.get("boundary")
    if not isinstance(boundary, list):
        raise SystemExit("boundary must be a list")
    boundary_text = "\n".join(str(x) for x in boundary)
    missing = [token for token in REQUIRED_BOUNDARY if token not in boundary_text]
    forbidden = [token for token in FORBIDDEN if token in boundary_text or token in raw]
    if missing:
        raise SystemExit(f"missing boundary tokens: {missing}")
    if forbidden:
        raise SystemExit(f"forbidden overclaim tokens: {forbidden}")

    print(f"Chronos COR incidence-basis certificate verification OK: {path}")


def main() -> None:
    verify_certificate(DEFAULT_CERT)


if __name__ == "__main__":
    main()
