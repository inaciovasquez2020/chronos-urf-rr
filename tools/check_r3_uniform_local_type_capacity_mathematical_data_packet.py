#!/usr/bin/env python3
import json
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "artifacts/chronos/r3_uniform_local_type_capacity_mathematical_data_packet_2026_05_24.json"

def fail(msg: str) -> None:
    raise SystemExit(f"R3_UNIFORM_LOCAL_TYPE_CAPACITY_PACKET_FAILED: {msg}")

def require(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)

def normalize_edge(e, vertices):
    require(isinstance(e, list) and len(e) == 2, "each edge must be a two-element list")
    a, b = e
    require(isinstance(a, str) and isinstance(b, str), "edge endpoints must be strings")
    require(a != b, "loops are not admissible")
    require(a in vertices and b in vertices, "edge endpoint outside vertex set")
    return tuple(sorted((a, b)))

def radius_ball(adj, start, radius):
    seen = {start: 0}
    q = deque([start])
    while q:
        node = q.popleft()
        if seen[node] >= radius:
            continue
        for nxt in adj[node]:
            if nxt not in seen:
                seen[nxt] = seen[node] + 1
                q.append(nxt)
    return seen

def local_type_signature(adj, labels, vertex, radius):
    ball = radius_ball(adj, vertex, radius)
    center_label = labels[vertex]
    neighbor_labels = sorted(labels[v] for v, d in ball.items() if v != vertex and d <= radius)
    return center_label + "|" + ",".join(neighbor_labels)

def main() -> None:
    packet_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not packet_path.is_absolute():
        packet_path = ROOT / packet_path

    try:
        data = json.loads(packet_path.read_text())
    except Exception as exc:
        fail(f"could not read packet: {exc}")

    require(data.get("artifact") == "R3_UNIFORM_LOCAL_TYPE_CAPACITY_MATHEMATICAL_DATA_PACKET", "wrong artifact")
    require(data.get("status") == "R3_DATA_PACKET_COMPUTABLE_NO_PROOF_CLAIM", "wrong status")
    require(data.get("target") == "UniformLocalTypeCapacityProofTarget", "wrong target")

    objects = data.get("objects")
    require(isinstance(objects, dict), "objects must be object")

    vertices = objects.get("vertices")
    require(isinstance(vertices, list) and vertices, "vertices must be nonempty")
    require(len(vertices) == len(set(vertices)), "vertices must be unique")
    vertex_set = set(vertices)

    edges = {normalize_edge(e, vertex_set) for e in objects.get("edges", [])}
    require(edges, "edges must be nonempty")

    labels = objects.get("labels")
    require(isinstance(labels, dict), "labels must be object")
    require(set(labels.keys()) == vertex_set, "every vertex must have exactly one label")

    alphabet = objects.get("type_alphabet")
    require(isinstance(alphabet, list) and alphabet, "type_alphabet must be nonempty list")
    alphabet_set = set(alphabet)
    require(all(label in alphabet_set for label in labels.values()), "all labels must lie in type_alphabet")

    radius = objects.get("local_type_radius")
    capacity_bound = objects.get("capacity_bound")
    require(isinstance(radius, int) and radius >= 0, "local_type_radius must be nonnegative integer")
    require(isinstance(capacity_bound, int) and capacity_bound > 0, "capacity_bound must be positive integer")

    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    signatures = {
        v: local_type_signature(adj, labels, v, radius)
        for v in vertices
    }
    distinct = sorted(set(signatures.values()))
    bound_ok = len(distinct) <= capacity_bound

    computed = data.get("computed_quantities")
    require(isinstance(computed, dict), "computed_quantities must be object")
    require(computed.get("local_type_signatures") == signatures, "local_type_signatures mismatch")
    require(computed.get("distinct_local_types") == distinct, "distinct_local_types mismatch")
    require(computed.get("distinct_local_type_count") == len(distinct), "distinct count mismatch")
    require(computed.get("capacity_bound") == capacity_bound, "capacity bound mismatch")
    require(computed.get("uniform_capacity_bound_satisfied") is bound_ok, "capacity flag mismatch")
    require(computed.get("computed_capacity_instance_present") is bound_ok, "instance flag mismatch")
    require(bound_ok, "uniform local-type capacity bound violated")

    boundary = data.get("does_not_prove", [])
    for token in [
        "general UniformLocalTypeCapacity",
        "native R1/R2/R3 instance",
        "P vs NP",
        "any Clay problem",
    ]:
        require(token in boundary, f"missing boundary token: {token}")

    print("R3_UNIFORM_LOCAL_TYPE_CAPACITY_PACKET_OK")

if __name__ == "__main__":
    main()
