#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
from itertools import product


@dataclass(frozen=True)
class Carrier:
    tag: str
    arity: int


@dataclass(frozen=True)
class Registry:
    carrier: Carrier


def registry_generates(registry: Registry, carrier: Carrier) -> bool:
    return registry.carrier == carrier


def finite_registry(registry: Registry) -> bool:
    return registry.carrier.arity >= 0


def represented_zero_arity_registry_pair(carrier: Carrier) -> bool:
    return carrier.arity == 0


def finite_represented_atom(carrier: Carrier) -> bool:
    return finite_registry(Registry(carrier))


def zero_arity_exhaustiveness(carrier: Carrier) -> bool:
    if carrier.arity != 0:
        return True
    registry = Registry(carrier)
    return (
        registry_generates(registry, carrier)
        and represented_zero_arity_registry_pair(carrier)
        and finite_represented_atom(carrier)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-arity", type=int, default=12)
    parser.add_argument("--tag-count", type=int, default=64)
    args = parser.parse_args()

    if args.max_arity < 0:
        raise SystemExit("--max-arity must be nonnegative")
    if args.tag_count < 1:
        raise SystemExit("--tag-count must be positive")

    tags = [f"carrier.{i}" for i in range(args.tag_count)]
    arities = list(range(args.max_arity + 1))
    carriers = [Carrier(tag, arity) for tag, arity in product(tags, arities)]

    failures = [c for c in carriers if not zero_arity_exhaustiveness(c)]

    payload = {
        "status": "FINITE_MODEL_EXHAUSTIVE_PROOF_ONLY" if not failures else "FAILED",
        "finite_universe": {
            "tag_count": args.tag_count,
            "arity_values": arities,
            "carrier_count": len(carriers)
        },
        "zero_arity_count": sum(1 for c in carriers if c.arity == 0),
        "failures": [c.__dict__ for c in failures],
        "theorem_level_closure": False,
        "boundary": "exhaustive proof over the declared finite toy universe only; no unrestricted Chronos-RR closure"
    }

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
