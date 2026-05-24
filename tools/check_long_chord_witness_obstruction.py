#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = {
    "status",
    "vertices",
    "edges",
    "diameter_bound",
    "long_chord_threshold",
    "claimed_long_chords_absent",
}

def fail(msg: str) -> None:
    raise SystemExit(f"LONG_CHORD_WITNESS_CHECK_FAILED: {msg}")

def load_packet(path: Path) -> dict:
    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        fail(f"could not read json: {exc}")
    missing = REQUIRED_TOP_LEVEL - set(data)
    if missing:
        fail(f"missing keys: {sorted(missing)}")
    return data

def normalize_edges(edges):
    out = set()
    for e in edges:
        if not isinstance(e, list) or len(e) != 2:
            fail("each edge must be a two-element list")
        a, b = e
        if a == b:
            fail("loops are not admissible")
        out.add(tuple(sorted((a, b))))
    return out

def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: check_long_chord_witness_obstruction.py PACKET.json")

    data = load_packet(Path(sys.argv[1]))

    if data["status"] != "FINITE_LONG_CHORD_WITNESS_PACKET":
        fail("status must be FINITE_LONG_CHORD_WITNESS_PACKET")

    vertices = data["vertices"]
    if not isinstance(vertices, list) or not vertices:
        fail("vertices must be a nonempty list")
    if len(set(vertices)) != len(vertices):
        fail("vertices must be unique")

    vertex_set = set(vertices)
    edges = normalize_edges(data["edges"])
    for a, b in edges:
        if a not in vertex_set or b not in vertex_set:
            fail("edge endpoint outside vertex set")

    diameter_bound = data["diameter_bound"]
    long_chord_threshold = data["long_chord_threshold"]
    if not isinstance(diameter_bound, int) or diameter_bound < 0:
        fail("diameter_bound must be a nonnegative integer")
    if not isinstance(long_chord_threshold, int) or long_chord_threshold <= diameter_bound:
        fail("long_chord_threshold must be an integer greater than diameter_bound")

    claimed_absent = data["claimed_long_chords_absent"]
    if claimed_absent is not True:
        fail("claimed_long_chords_absent must be true")

    declared_long_chords = data.get("declared_long_chords", [])
    if declared_long_chords:
        fail("declared_long_chords must be empty for an absence certificate")

    print("LONG_CHORD_WITNESS_CHECK_OK")

if __name__ == "__main__":
    main()
