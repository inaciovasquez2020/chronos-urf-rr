"""Exact structural coverage auditor over GF(2).

Structural coverage is not a measure of factual accuracy.
"""

from collections import deque
from fractions import Fraction
from itertools import combinations


class IncompleteAudit(RuntimeError):
    pass


class BinaryBasis:
    def __init__(self, tick=None):
        self.rows = {}
        self.tick = tick

    def add(self, value):
        while value:
            if self.tick is not None:
                self.tick()
            pivot = value.bit_length() - 1
            if pivot in self.rows:
                value ^= self.rows[pivot]
            else:
                self.rows[pivot] = value
                return True
        return False

    @property
    def rank(self):
        return len(self.rows)


class RadiusAuditor:
    def __init__(
        self, vertices, edges,
        max_vertices=256,
        max_edges=4096,
        max_work=5_000_000
    ):
        for limit in (max_vertices, max_edges, max_work):
            if type(limit) is not int or limit <= 0:
                raise ValueError("Invalid resource limit")

        self.max_work = max_work
        self.work = 0

        vertex_set = set()

        for v in vertices:
            self.tick()

            if type(v) not in (int, str):
                raise ValueError("Invalid vertex identifier")

            vertex_set.add(v)

            if len(vertex_set) > max_vertices:
                raise IncompleteAudit("Vertex guard exceeded")

        if len({type(v) for v in vertex_set}) > 1:
            raise ValueError("Mixed vertex identifier types")

        self.vertices = tuple(sorted(vertex_set))

        edge_set = set()

        for a, b in edges:
            self.tick()
            if a == b:
                raise ValueError("Self-loops are unsupported")
            if a not in self.vertices or b not in self.vertices:
                raise ValueError("Unknown vertex")
            edge_set.add(tuple(sorted((a, b))))

            if len(edge_set) > max_edges:
                raise IncompleteAudit("Edge guard exceeded")

        self.edges = tuple(sorted(edge_set))

        if len(self.vertices) > max_vertices:
            raise IncompleteAudit("Vertex guard exceeded")

        if len(self.edges) > max_edges:
            raise IncompleteAudit("Edge guard exceeded")

        self.adj = {v: [] for v in self.vertices}

        for i, (a, b) in enumerate(self.edges):
            self.adj[a].append((b, i))
            self.adj[b].append((a, i))

    def tick(self):
        self.work += 1
        if self.work > self.max_work:
            raise IncompleteAudit("Work guard exceeded")

    def dimension(self):
        seen = set()
        components = 0

        for root in self.vertices:
            if root in seen:
                continue

            components += 1
            seen.add(root)
            queue = deque([root])

            while queue:
                a = queue.popleft()
                for b, _ in self.adj[a]:
                    self.tick()
                    if b not in seen:
                        seen.add(b)
                        queue.append(b)

        return (
            len(self.edges)
            - len(self.vertices)
            + components
        )

    def local_basis(self, radius):
        if type(radius) is not int or radius < 0:
            raise ValueError("Invalid radius")

        basis = BinaryBasis(self.tick)

        for root in self.vertices:
            depth = {root: 0}
            paths = {root: 0}
            queue = deque([root])

            while queue:
                a = queue.popleft()

                if depth[a] == radius:
                    continue

                for b, i in self.adj[a]:
                    self.tick()

                    if b not in depth:
                        depth[b] = depth[a] + 1
                        paths[b] = paths[a] ^ (1 << i)
                        queue.append(b)

            for i, (a, b) in enumerate(self.edges):
                self.tick()

                if a not in depth or b not in depth:
                    continue

                cycle = (
                    paths[a]
                    ^ (1 << i)
                    ^ paths[b]
                )

                assert bin(cycle).count("1") <= 2 * radius + 1

                basis.add(cycle)

        return basis

    def audit(self, radius):
        total = self.dimension()
        local = self.local_basis(radius).rank

        assert 0 <= local <= total

        return {
            "radius": radius,
            "support_cutoff": 2 * radius + 1,
            "total_dimension": total,
            "local_dimension": local,
            "unresolved_dimension": total - local,
            "coverage": (
                str(Fraction(local, total))
                if total else None
            ),
            "cycle_space_saturated": local == total,
            "factual_accuracy": "NOT_MEASURED",
            "status": "COMPLETE",
        }

    def adaptive(self, max_radius):
        if type(max_radius) is not int or max_radius < 0:
            raise ValueError("Invalid radius limit")

        results = []

        for radius in range(
            min(max_radius, len(self.vertices)) + 1
        ):
            result = self.audit(radius)

            if results:
                assert (
                    result["local_dimension"]
                    >= results[-1]["local_dimension"]
                )

            results.append(result)

            if result["cycle_space_saturated"]:
                return {
                    "status": "SATURATED",
                    "profile": results,
                }

        return {
            "status": "RADIUS_LIMIT_REACHED",
            "profile": results,
        }


def independent_oracle(vertices, edges, radius):
    """Exhaustively enumerate bounded-support GF(2) cycles."""

    rank = BinaryBasis()
    cutoff = min(2 * radius + 1, len(edges))

    for size in range(1, cutoff + 1):
        for subset in combinations(range(len(edges)), size):
            odd = set()
            vector = 0

            for i in subset:
                a, b = edges[i]

                odd.symmetric_difference_update((a, b))
                vector |= 1 << i

            if not odd:
                rank.add(vector)

    return rank.rank
