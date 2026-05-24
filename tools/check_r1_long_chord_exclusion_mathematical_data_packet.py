#!/usr/bin/env python3
import json
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "artifacts/chronos/r1_long_chord_exclusion_mathematical_data_packet_2026_05_24.json"

def fail(msg: str) -> None:
    raise SystemExit(f"R1_LONG_CHORD_DATA_PACKET_FAILED: {msg}")

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

def graph_distance(adj, start, end):
    if start == end:
        return 0
    seen = {start}
    q = deque([(start, 0)])
    while q:
        node, dist = q.popleft()
        for nxt in adj[node]:
            if nxt == end:
                return dist + 1
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, dist + 1))
    return None

def main() -> None:
    packet_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not packet_path.is_absolute():
        packet_path = ROOT / packet_path

    try:
        data = json.loads(packet_path.read_text())
    except Exception as exc:
        fail(f"could not read packet: {exc}")

    require(data.get("artifact") == "R1_LONG_CHORD_EXCLUSION_MATHEMATICAL_DATA_PACKET", "wrong artifact")
    require(data.get("status") == "R1_DATA_PACKET_COMPUTABLE_NO_PROOF_CLAIM", "wrong status")
    require(data.get("target") == "LongChordExclusionProofTarget", "wrong target")

    objects = data.get("objects")
    require(isinstance(objects, dict), "objects must be object")

    vertices = objects.get("vertices")
    require(isinstance(vertices, list) and vertices, "vertices must be nonempty list")
    require(len(vertices) == len(set(vertices)), "vertices must be unique")
    vertex_set = set(vertices)

    skeleton_edges = {normalize_edge(e, vertex_set) for e in objects.get("skeleton_edges", [])}
    candidate_chords = {normalize_edge(e, vertex_set) for e in objects.get("candidate_chords", [])}
    require(skeleton_edges, "skeleton_edges must be nonempty")
    require(candidate_chords, "candidate_chords must be nonempty")

    threshold = objects.get("long_chord_threshold")
    require(isinstance(threshold, int) and threshold > 0, "long_chord_threshold must be positive integer")

    adj = {v: set() for v in vertices}
    for a, b in skeleton_edges:
        adj[a].add(b)
        adj[b].add(a)

    distances = {}
    long_chords = []
    for a, b in sorted(candidate_chords):
        d = graph_distance(adj, a, b)
        require(d is not None, f"candidate endpoints disconnected: {a}, {b}")
        distances[edge_key(a, b)] = d
        if d >= threshold:
            long_chords.append([a, b])

    computed = data.get("computed_quantities")
    require(isinstance(computed, dict), "computed_quantities must be object")
    require(computed.get("candidate_distances") == distances, "candidate_distances mismatch")
    require(computed.get("max_candidate_skeleton_distance") == max(distances.values()), "max distance mismatch")
    require(computed.get("long_chord_threshold") == threshold, "threshold mismatch")
    require(computed.get("computed_long_chords") == long_chords, "computed long chords mismatch")
    require(computed.get("computed_long_chords_absent") is (len(long_chords) == 0), "absence flag mismatch")
    require(not long_chords, "long chord witness exists")

    boundary = data.get("does_not_prove", [])
    for token in [
        "general LongChordExclusion",
        "native R1/R2/R3 instance",
        "P vs NP",
        "any Clay problem",
    ]:
        require(token in boundary, f"missing boundary token: {token}")

    print("R1_LONG_CHORD_DATA_PACKET_OK")

if __name__ == "__main__":
    main()
