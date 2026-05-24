#!/usr/bin/env python3
import json
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "artifacts/chronos/r2_diameter_separation_filling_mathematical_data_packet_2026_05_24.json"

def fail(msg: str) -> None:
    raise SystemExit(f"R2_DIAMETER_SEPARATION_FILLING_PACKET_FAILED: {msg}")

def require(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)

def edge_key(a: str, b: str) -> str:
    x, y = sorted((a, b))
    return f"{x}--{y}"

def normalize_edge(e, vertices):
    require(isinstance(e, list) and len(e) == 2, "each edge must be a two-element list")
    a, b = e
    require(isinstance(a, str) and isinstance(b, str), "edge endpoints must be strings")
    require(a != b, "loops are not admissible")
    require(a in vertices and b in vertices, "edge endpoint outside vertex set")
    return tuple(sorted((a, b)))

def bfs_distances(adj, start):
    seen = {start: 0}
    q = deque([start])
    while q:
        node = q.popleft()
        for nxt in adj[node]:
            if nxt not in seen:
                seen[nxt] = seen[node] + 1
                q.append(nxt)
    return seen

def main() -> None:
    packet_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not packet_path.is_absolute():
        packet_path = ROOT / packet_path

    try:
        data = json.loads(packet_path.read_text())
    except Exception as exc:
        fail(f"could not read packet: {exc}")

    require(data.get("artifact") == "R2_DIAMETER_SEPARATION_FILLING_MATHEMATICAL_DATA_PACKET", "wrong artifact")
    require(data.get("status") == "R2_DATA_PACKET_COMPUTABLE_NO_PROOF_CLAIM", "wrong status")
    require(data.get("target") == "DiameterSeparationFillingObstructionProofTarget", "wrong target")

    objects = data.get("objects")
    require(isinstance(objects, dict), "objects must be object")

    vertices = objects.get("vertices")
    require(isinstance(vertices, list) and vertices, "vertices must be nonempty")
    require(len(vertices) == len(set(vertices)), "vertices must be unique")
    vertex_set = set(vertices)

    edges = {normalize_edge(e, vertex_set) for e in objects.get("edges", [])}
    require(edges, "edges must be nonempty")

    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    all_dist = {v: bfs_distances(adj, v) for v in vertices}
    require(all(len(d) == len(vertices) for d in all_dist.values()), "graph must be connected")

    graph_diameter = max(max(d.values()) for d in all_dist.values())

    diameter_bound = objects.get("diameter_bound")
    separation_threshold = objects.get("separation_threshold")
    filling_floor = objects.get("filling_floor")
    require(isinstance(diameter_bound, int) and diameter_bound >= 0, "diameter_bound must be nonnegative integer")
    require(isinstance(separation_threshold, int) and separation_threshold >= 0, "separation_threshold must be nonnegative integer")
    require(isinstance(filling_floor, int) and filling_floor >= 0, "filling_floor must be nonnegative integer")

    terminal_pairs = [normalize_edge(e, vertex_set) for e in objects.get("terminal_pairs", [])]
    require(terminal_pairs, "terminal_pairs must be nonempty")

    terminal_distances = {}
    for a, b in terminal_pairs:
        terminal_distances[edge_key(a, b)] = all_dist[a][b]

    filling_certs = objects.get("filling_certificates")
    require(isinstance(filling_certs, dict), "filling_certificates must be object")

    filling_sizes = {}
    for a, b in terminal_pairs:
        key = edge_key(a, b)
        cert = filling_certs.get(key)
        require(isinstance(cert, list) and cert, f"missing filling certificate for {key}")
        normalized = [normalize_edge(e, vertex_set) for e in cert]
        for edge in normalized:
            require(edge in edges, f"filling certificate uses non-edge for {key}")
        filling_sizes[key] = len(normalized)

    computed = data.get("computed_quantities")
    require(isinstance(computed, dict), "computed_quantities must be object")

    diameter_ok = graph_diameter <= diameter_bound
    separation_ok = min(terminal_distances.values()) >= separation_threshold
    filling_ok = min(filling_sizes.values()) > filling_floor
    obstruction_present = diameter_ok and separation_ok and filling_ok

    require(computed.get("graph_diameter") == graph_diameter, "graph_diameter mismatch")
    require(computed.get("terminal_distances") == terminal_distances, "terminal_distances mismatch")
    require(computed.get("minimum_terminal_separation") == min(terminal_distances.values()), "minimum separation mismatch")
    require(computed.get("filling_sizes") == filling_sizes, "filling_sizes mismatch")
    require(computed.get("minimum_filling_size") == min(filling_sizes.values()), "minimum filling size mismatch")
    require(computed.get("diameter_bound_satisfied") is diameter_ok, "diameter flag mismatch")
    require(computed.get("separation_threshold_satisfied") is separation_ok, "separation flag mismatch")
    require(computed.get("filling_floor_obstruction_satisfied") is filling_ok, "filling flag mismatch")
    require(computed.get("computed_obstruction_present") is obstruction_present, "obstruction flag mismatch")
    require(obstruction_present, "computed obstruction is absent")

    boundary = data.get("does_not_prove", [])
    for token in [
        "general DiameterSeparationFillingObstruction",
        "native R1/R2/R3 instance",
        "P vs NP",
        "any Clay problem",
    ]:
        require(token in boundary, f"missing boundary token: {token}")

    print("R2_DIAMETER_SEPARATION_FILLING_PACKET_OK")

if __name__ == "__main__":
    main()
