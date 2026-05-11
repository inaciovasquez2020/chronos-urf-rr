#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SKIP_FILES = {
    "Chronos/Frontier/ZeroArityCarrierExhaustivenessConditional.lean",
    "Chronos/Frontier/RepositoryNativeZeroArityCarrierMigrationTarget.lean",
    "Chronos/Frontier/RepositoryNativeZeroArityInterfaceAudit.lean",
}

FIELD_PATTERNS = {
    "Carrier": re.compile(r"\b(inductive|structure|abbrev|def)\s+[A-Za-z0-9_]*Carrier\b"),
    "Registry": re.compile(r"\b(inductive|structure|abbrev|def)\s+[A-Za-z0-9_]*Registry\b"),
    "arity": re.compile(r"\barity\b"),
    "carrierRegistry": re.compile(r"\bcarrierRegistry\b|\b[A-Za-z0-9_]*Registry\b"),
    "registryGenerates": re.compile(r"\bregistryGenerates\b|\bRegistryGenerates\b"),
    "finiteRegistry": re.compile(r"\bfiniteRegistry\b|\bFiniteRegistry\b"),
    "representedZeroArityRegistryPair": re.compile(r"\brepresentedZeroArityRegistryPair\b|\bRepresentedZeroArityRegistryPair\b"),
    "isFiniteRepresentedAtom": re.compile(r"\bisFiniteRepresentedAtom\b|\bIsFiniteRepresentedAtom\b"),
    "carrierRegistryGenerates": re.compile(r"\bcarrierRegistryGenerates\b|\bCarrierRegistryGeneration\b"),
    "finiteRegistryCarrier": re.compile(r"\bfiniteRegistryCarrier\b|\bfinite_registry_carrier\b"),
    "representedZeroArityOfArityZero": re.compile(r"\brepresentedZeroArityOfArityZero\b|\brepresented_zero_arity_registry_pair_of_arity_zero\b"),
    "finiteRepresentedAtomOfFiniteRegistry": re.compile(r"\bfiniteRepresentedAtomOfFiniteRegistry\b|\bfinite_represented_atom_of_finite_registry\b"),
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def scan() -> dict[str, list[str]]:
    candidates: dict[str, list[str]] = {field: [] for field in FIELD_PATTERNS}

    for path in sorted((ROOT / "Chronos").rglob("*.lean")):
        relative = rel(path)
        if relative in SKIP_FILES:
            continue

        text = path.read_text(errors="replace")
        for field, pattern in FIELD_PATTERNS.items():
            if pattern.search(text):
                candidates[field].append(relative)

    return candidates


def main() -> int:
    candidates = scan()
    missing = [field for field, hits in candidates.items() if not hits]

    payload = {
        "status": "FRONTIER_OPEN / ACTIVE_NATIVE_INTERFACE_AUDIT_ONLY",
        "all_required_fields_bound": not missing,
        "missing_fields": missing,
        "candidate_files": candidates,
        "weakest_missing_object": (
            "none_detected_by_static_scan"
            if not missing
            else "active repository-native fields missing from static scan"
        ),
        "theorem_level_closure": False,
        "boundary": "static audit only; no active RepositoryNativeZeroArityInterface instantiation; no unrestricted Chronos-RR closure"
    }

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
