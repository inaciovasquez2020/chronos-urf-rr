#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path


RADIUS = 2
LOCAL_CYCLE_CUTOFF = 2 * RADIUS + 1
OUT = Path("artifacts/fgl/source_matrices.json")
META = Path("artifacts/fgl/petersen_2lift_fgl_source_metadata.json")
STATUS = Path("docs/status/FGL_PETERSEN_INSTANCE_STATUS_2026_04_27.md")


def petersen_base_edges():
    edges = set()

    def add(u: int, v: int) -> None:
        if u > v:
            u, v = v, u
        edges.add((u, v))

    for i in range(5):
        add(i, (i + 1) % 5)
        add(i, i + 5)

    for i in range(5):
        add(i + 5, ((i + 2) % 5) + 5)

    return sorted(edges)


def lift_edges(base_edges, twisted_edges):
    out = set()

    for u, v in base_edges:
        for b in (0, 1):
            if (u, v) in twisted_edges:
                a = (u, b)
                c = (v, 1 - b)
            else:
                a = (u, b)
                c = (v, b)

            if a > c:
                a, c = c, a

            out.add((a, c))

    return sorted(out)


def adjacency_with_edges(edges):
    adj = defaultdict(list)

    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))

    return {k: sorted(vs) for k, vs in adj.items()}


def adjacency(edges):
    adj = defaultdict(set)

    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    return {k: sorted(vs) for k, vs in adj.items()}


def edge_index(edges):
    return {e: i for i, e in enumerate(edges)}


def canonical_cycle(cycle):
    n = len(cycle)
    seqs = []

    for seq in (cycle, list(reversed(cycle))):
        m = min(range(n), key=lambda i: seq[i])
        seqs.append(tuple(seq[m:] + seq[:m]))

    return min(seqs)


def simple_cycles_up_to(adj, max_len):
    nodes = sorted(adj)
    cycles = set()

    def dfs(start, cur, path, seen):
        for nb in adj[cur]:
            if nb == start and len(path) >= 3:
                cycles.add(canonical_cycle(path[:]))
            elif nb not in seen and len(path) < max_len and nb >= start:
                seen.add(nb)
                path.append(nb)
                dfs(start, nb, path, seen)
                path.pop()
                seen.remove(nb)

    for start in nodes:
        dfs(start, start, [start], {start})

    return sorted(c for c in cycles if len(c) <= max_len)


def cycle_vector(cycle, eidx):
    vec = [0] * len(eidx)
    n = len(cycle)

    for i in range(n):
        a = cycle[i]
        b = cycle[(i + 1) % n]

        if a > b:
            a, b = b, a

        vec[eidx[(a, b)]] ^= 1

    return vec


def fundamental_cycle_basis(edges):
    adj = adjacency_with_edges(edges)
    parent = {}
    parent_edge = {}
    depth = {}
    tree_edges = set()
    visited = set()
    basis = []

    for root in sorted(adj):
        if root in visited:
            continue

        parent[root] = None
        parent_edge[root] = None
        depth[root] = 0
        visited.add(root)
        q = deque([root])

        while q:
            u = q.popleft()

            for v, edge_id in adj[u]:
                if v not in visited:
                    visited.add(v)
                    parent[v] = u
                    parent_edge[v] = edge_id
                    depth[v] = depth[u] + 1
                    tree_edges.add(edge_id)
                    q.append(v)

    for edge_id, (u, v) in enumerate(edges):
        if edge_id in tree_edges:
            continue

        vec = [0] * len(edges)
        vec[edge_id] = 1

        a = u
        b = v

        while depth[a] > depth[b]:
            vec[parent_edge[a]] ^= 1
            a = parent[a]

        while depth[b] > depth[a]:
            vec[parent_edge[b]] ^= 1
            b = parent[b]

        while a != b:
            vec[parent_edge[a]] ^= 1
            a = parent[a]
            vec[parent_edge[b]] ^= 1
            b = parent[b]

        basis.append(vec)

    return basis


def gf2_rref_matrix(A):
    A = [row[:] for row in A]

    if not A:
        return A, []

    m = len(A)
    n = len(A[0])
    pivots = []
    r = 0

    for c in range(n):
        pivot = None

        for i in range(r, m):
            if A[i][c]:
                pivot = i
                break

        if pivot is None:
            continue

        A[r], A[pivot] = A[pivot], A[r]

        for i in range(m):
            if i != r and A[i][c]:
                A[i] = [x ^ y for x, y in zip(A[i], A[r])]

        pivots.append(c)
        r += 1

        if r == m:
            break

    return A, pivots


def gf2_rref_basis(vectors):
    R, _ = gf2_rref_matrix(vectors)
    return [row for row in R if any(row)]


def gf2_rank(vectors):
    return len(gf2_rref_basis(vectors))


def gf2_nullspace(A):
    if not A:
        return []

    R, pivots = gf2_rref_matrix(A)
    n = len(A[0])
    pivot_set = set(pivots)
    free_cols = [j for j in range(n) if j not in pivot_set]
    basis = []

    for free in free_cols:
        x = [0] * n
        x[free] = 1

        for row_index, pivot_col in enumerate(pivots):
            x[pivot_col] = R[row_index][free]

        basis.append(x)

    return basis


def gf2_solve_rows(row_basis, target):
    d = len(row_basis)
    A = [[row_basis[j][i] for j in range(d)] + [target[i]] for i in range(len(target))]
    R, pivots = gf2_rref_matrix(A)

    for row in R:
        if all(x == 0 for x in row[:d]) and row[d] == 1:
            raise ValueError("target vector is not in row span")

    x = [0] * d

    for row_index, pivot_col in enumerate(pivots):
        if pivot_col < d:
            x[pivot_col] = R[row_index][d]

    return x


def build_instance():
    base_edges = petersen_base_edges()
    edges = lift_edges(base_edges, {(0, 1)})
    adj = adjacency(edges)
    eidx = edge_index(edges)

    global_cycle_basis = fundamental_cycle_basis(edges)
    global_dim = len(global_cycle_basis)

    local_cycles = simple_cycles_up_to(adj, LOCAL_CYCLE_CUTOFF)
    local_vectors = [cycle_vector(c, eidx) for c in local_cycles]
    local_basis = gf2_rref_basis(local_vectors)
    local_dim = len(local_basis)

    local_coords = [gf2_solve_rows(global_cycle_basis, v) for v in local_basis]

    witness_matrix = [
        [local_coords[col][row] for col in range(local_dim)]
        for row in range(global_dim)
    ]

    witness_transpose = [
        [witness_matrix[row][col] for row in range(global_dim)]
        for col in range(local_dim)
    ]

    functionals = gf2_nullspace(witness_transpose)

    if not functionals:
        functionals = [[0] * global_dim]

    test_matrix_basis_by_test = [
        [functionals[col][row] for col in range(len(functionals))]
        for row in range(global_dim)
    ]

    metadata = {
        "status": "finite_instance_only",
        "field": "GF(2)",
        "instance": "Petersen 2-lift, G_minus, twisted edge (0,1)",
        "radius": RADIUS,
        "local_cycle_cutoff": LOCAL_CYCLE_CUTOFF,
        "edge_count": len(edges),
        "cycle_space_dimension": global_dim,
        "local_cycle_span_dimension": local_dim,
        "quotient_dimension": global_dim - local_dim,
        "test_count": len(functionals),
        "meaning": (
            "E is the GF(2) cycle space of G_minus; witness columns span the "
            "local cycle subspace generated by cycles of length <= 2R+1; test "
            "columns are separating linear functionals for the quotient."
        ),
        "non_claim": (
            "This is not a general H4.1 proof and does not certify local "
            "indistinguishability or tree-ball hypotheses."
        ),
    }

    source = {
        "field": "GF(2)",
        "test_matrix_basis_by_test": test_matrix_basis_by_test,
        "witness_matrix": witness_matrix,
        "metadata": metadata,
    }

    return source, metadata


def main() -> int:
    source, metadata = build_instance()

    if metadata["cycle_space_dimension"] != 11:
        raise SystemExit("unexpected cycle-space dimension")

    if metadata["local_cycle_span_dimension"] != 10:
        raise SystemExit("unexpected local-cycle span dimension")

    if metadata["quotient_dimension"] != 1:
        raise SystemExit("unexpected quotient dimension")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    META.parent.mkdir(parents=True, exist_ok=True)
    STATUS.parent.mkdir(parents=True, exist_ok=True)

    OUT.write_text(json.dumps(source, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    META.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    STATUS.write_text(
        "# FGL Petersen finite-instance status — 2026-04-27\n\n"
        "Status: Conditional at theorem level; finite matrix source exported.\n\n"
        "This records only the Petersen 2-lift `G_minus` finite-instance linear-algebra certificate.\n\n"
        "It does not prove general H4.1, R1, R2, or R3.\n\n"
        "It does not certify local indistinguishability or tree-ball hypotheses.\n\n"
        "Generated files:\n\n"
        "- `artifacts/fgl/source_matrices.json`\n"
        "- `artifacts/fgl/petersen_2lift_fgl_source_metadata.json`\n\n"
        f"Cycle-space dimension: {metadata['cycle_space_dimension']}\n\n"
        f"Local-cycle span dimension: {metadata['local_cycle_span_dimension']}\n\n"
        f"Quotient dimension: {metadata['quotient_dimension']}\n\n",
        encoding="utf-8",
    )

    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
