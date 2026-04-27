#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class BallVolumeCertificate:
    n: int
    root: int
    radius: int
    delta_bound: int
    max_degree: int
    ball_cardinality: int
    volume_bound: int
    girth: int | None
    hypothesis_girth_gt_ball_card: bool
    hypothesis_girth_gt_volume_bound: bool
    ball_acyclic: bool
    old_two_r_bound_counterexample: bool


def normalize_edges(edges: Iterable[tuple[int, int]]) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
    for a, b in edges:
        if a == b:
            raise ValueError("loops are not supported")
        if a > b:
            a, b = b, a
        out.add((a, b))
    return out


def adjacency(n: int, edges: set[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for a, b in edges:
        if not (0 <= a < n and 0 <= b < n):
            raise ValueError("edge endpoint out of range")
        adj[a].add(b)
        adj[b].add(a)
    return adj


def max_degree(n: int, edges: set[tuple[int, int]]) -> int:
    return max((len(nei) for nei in adjacency(n, edges)), default=0)


def ball_vertices(n: int, edges: set[tuple[int, int]], root: int, radius: int) -> set[int]:
    adj = adjacency(n, edges)
    dist = {root: 0}
    q = deque([root])

    while q:
        x = q.popleft()
        if dist[x] == radius:
            continue
        for y in adj[x]:
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)

    return set(dist)


def induced_edges(edges: set[tuple[int, int]], verts: set[int]) -> set[tuple[int, int]]:
    return {(a, b) for a, b in edges if a in verts and b in verts}


def is_acyclic(n: int, edges: set[tuple[int, int]], verts: set[int] | None = None) -> bool:
    if verts is None:
        verts = set(range(n))

    adj = {v: set() for v in verts}
    for a, b in induced_edges(edges, verts):
        adj[a].add(b)
        adj[b].add(a)

    seen: set[int] = set()

    for start in sorted(verts):
        if start in seen:
            continue
        parent = {start: None}
        seen.add(start)
        stack = [start]

        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y == parent[x]:
                    continue
                if y in seen:
                    return False
                seen.add(y)
                parent[y] = x
                stack.append(y)

    return True


def girth(n: int, edges: set[tuple[int, int]]) -> int | None:
    adj = adjacency(n, edges)
    best: int | None = None

    for s in range(n):
        dist = [-1] * n
        parent = [-1] * n
        dist[s] = 0
        q = deque([s])

        while q:
            x = q.popleft()
            for y in adj[x]:
                if dist[y] == -1:
                    dist[y] = dist[x] + 1
                    parent[y] = x
                    q.append(y)
                elif parent[x] != y and parent[y] != x:
                    cand = dist[x] + dist[y] + 1
                    best = cand if best is None else min(best, cand)

    return best


def volume_bound(delta: int, radius: int) -> int:
    if radius == 0:
        return 1
    if delta <= 0:
        return 1
    if delta == 1:
        return 2
    return 1 + delta * sum((delta - 1) ** j for j in range(radius))


def certify(n: int, edges_raw: Iterable[tuple[int, int]], root: int, radius: int, delta_bound: int) -> BallVolumeCertificate:
    edges = normalize_edges(edges_raw)
    md = max_degree(n, edges)
    if md > delta_bound:
        raise ValueError(f"max degree {md} exceeds delta bound {delta_bound}")

    B = ball_vertices(n, edges, root, radius)
    ball_edges = induced_edges(edges, B)
    g = girth(n, edges)
    vb = volume_bound(delta_bound, radius)
    ball_acyc = is_acyclic(n, edges, B)

    hyp_ball = g is not None and g > len(B)
    hyp_vol = g is not None and g > vb

    if len(B) > vb:
        raise AssertionError("ball cardinality exceeded bounded-degree volume bound")

    if hyp_ball and not ball_acyc:
        raise AssertionError("girth > |Ball| but induced ball has a cycle")

    if hyp_vol and not ball_acyc:
        raise AssertionError("girth > volume_bound but induced ball has a cycle")

    old_counterexample = False
    if not ball_acyc and g is not None and g > 2 * radius:
        old_counterexample = True

    return BallVolumeCertificate(
        n=n,
        root=root,
        radius=radius,
        delta_bound=delta_bound,
        max_degree=md,
        ball_cardinality=len(B),
        volume_bound=vb,
        girth=g,
        hypothesis_girth_gt_ball_card=hyp_ball,
        hypothesis_girth_gt_volume_bound=hyp_vol,
        ball_acyclic=ball_acyc,
        old_two_r_bound_counterexample=old_counterexample,
    )


def main() -> int:
    cases = {
        "triangle_R1_old_bound_counterexample": certify(
            3,
            [(0, 1), (1, 2), (2, 0)],
            root=0,
            radius=1,
            delta_bound=2,
        ),
        "path_R2_acyclic": certify(
            5,
            [(0, 1), (1, 2), (2, 3), (3, 4)],
            root=2,
            radius=2,
            delta_bound=2,
        ),
        "cycle6_R1_ball_acyclic": certify(
            6,
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)],
            root=0,
            radius=1,
            delta_bound=2,
        ),
    }

    out = Path("artifacts/ball_volume_acyclicity/certificates.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps({k: asdict(v) for k, v in cases.items()}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    assert cases["triangle_R1_old_bound_counterexample"].old_two_r_bound_counterexample is True
    assert cases["path_R2_acyclic"].ball_acyclic is True
    assert cases["cycle6_R1_ball_acyclic"].ball_acyclic is True

    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
