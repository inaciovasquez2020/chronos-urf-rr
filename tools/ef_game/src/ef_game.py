from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional, Set, FrozenSet
import json, hashlib

Vertex = int
Pebble = int

@dataclass(frozen=True)
class GameSpec:
    k: int
    rounds: int
    graphA: Dict[Vertex, List[Vertex]]
    graphB: Dict[Vertex, List[Vertex]]
    seed: int = 0

def _canon_adj(G: Dict[int, List[int]]) -> Dict[int, Tuple[int, ...]]:
    return {int(v): tuple(sorted(map(int, nbrs))) for v, nbrs in sorted(G.items())}

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def spec_digest(spec: GameSpec) -> str:
    payload = {
        "k": spec.k,
        "rounds": spec.rounds,
        "A": _canon_adj(spec.graphA),
        "B": _canon_adj(spec.graphB),
        "seed": spec.seed,
    }
    b = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(b)

def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="outp", required=True)
    args = ap.parse_args()
    data = json.load(open(args.inp, "r", encoding="utf-8"))
    spec = GameSpec(
        k=int(data["k"]),
        rounds=int(data["rounds"]),
        graphA={int(k): list(map(int,v)) for k,v in data["A"].items()},
        graphB={int(k): list(map(int,v)) for k,v in data["B"].items()},
        seed=int(data.get("seed", 0)),
    )
    out = {
        "spec_sha256": spec_digest(spec),
        "status": "TODO_solver",
    }
    json.dump(out, open(args.outp, "w", encoding="utf-8"), indent=2, sort_keys=True)
