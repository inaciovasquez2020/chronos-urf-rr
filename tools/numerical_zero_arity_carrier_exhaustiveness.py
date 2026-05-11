#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import json


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
    return isinstance(registry.carrier.arity, int) and registry.carrier.arity >= 0


def represented_zero_arity_registry_pair(carrier: Carrier) -> bool:
    return carrier.arity == 0


def finite_represented_atom(carrier: Carrier) -> bool:
    return finite_registry(Registry(carrier))


def zero_arity_exhaustiveness_holds(carrier: Carrier) -> bool:
    if carrier.arity != 0:
        return True
    registry = Registry(carrier)
    return (
        registry_generates(registry, carrier)
        and represented_zero_arity_registry_pair(carrier)
        and finite_represented_atom(carrier)
    )


def main() -> int:
    carriers = [
        Carrier("zero.unit", 0),
        Carrier("zero.empty", 0),
        Carrier("positive.unary", 1),
        Carrier("positive.binary", 2),
    ]

    failures = [c for c in carriers if not zero_arity_exhaustiveness_holds(c)]

    result = {
        "status": "NUMERICAL_SANITY_ONLY" if not failures else "FAILED",
        "tested_carriers": [c.__dict__ for c in carriers],
        "zero_arity_count": sum(1 for c in carriers if c.arity == 0),
        "failures": [c.__dict__ for c in failures],
        "theorem_level_closure": False,
        "boundary": "finite toy-model sanity check only; no unrestricted Chronos-RR closure"
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
