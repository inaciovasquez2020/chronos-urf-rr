#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        import toml_compat as tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


STATUS_DISCHARGED = "DISCHARGED_SURFACE"
STATUS_CONDITIONAL = "CONDITIONAL_SURFACE"
STATUS_OPEN = "FRONTIER_OPEN"


@dataclass(frozen=True)
class SurfaceInventory:
    name: str
    module: str | None
    axioms: list[str]
    placeholders: list[str]


def _load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as f:
        return tomllib.load(f)


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x) for x in value]
    return [str(value)]


def _parse_inventory(raw: str) -> dict[str, SurfaceInventory]:
    current: str | None = None
    modules: dict[str, str | None] = {}
    axioms: dict[str, set[str]] = {}
    placeholders: dict[str, set[str]] = {}

    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        m = re.match(r"^SURFACE\s+([A-Za-z0-9_.:-]+)$", stripped)
        if m:
            current = m.group(1)
            modules.setdefault(current, None)
            axioms.setdefault(current, set())
            placeholders.setdefault(current, set())
            continue

        m = re.match(r"^MODULE\s+([A-Za-z0-9_.:-]+)\s+([A-Za-z0-9_.:-]+)$", stripped)
        if m:
            surface, module = m.group(1), m.group(2)
            modules[surface] = module
            axioms.setdefault(surface, set())
            placeholders.setdefault(surface, set())
            current = surface
            continue

        m = re.match(r"^AXIOM\s+([A-Za-z0-9_.:-]+)(?:\s+(.+))?$", stripped)
        if m:
            if current is None:
                current = "unscoped"
                modules.setdefault(current, None)
                axioms.setdefault(current, set())
                placeholders.setdefault(current, set())
            axiom = (m.group(2) or m.group(1)).strip()
            axioms.setdefault(current, set()).add(axiom)
            continue

        m = re.match(r"^(SORRY|ADMIT|PLACEHOLDER)\s+(.+)$", stripped)
        if m:
            if current is None:
                current = "unscoped"
                modules.setdefault(current, None)
                axioms.setdefault(current, set())
                placeholders.setdefault(current, set())
            placeholders.setdefault(current, set()).add(m.group(2).strip())
            continue

    return {
        name: SurfaceInventory(
            name=name,
            module=modules.get(name),
            axioms=sorted(axioms.get(name, set())),
            placeholders=sorted(placeholders.get(name, set())),
        )
        for name in sorted(set(modules) | set(axioms) | set(placeholders))
    }


def _surface_status(open_axioms: list[str], open_placeholders: list[str], declared_status: str) -> str:
    if declared_status == STATUS_OPEN:
        return STATUS_OPEN
    if open_axioms or open_placeholders:
        return STATUS_CONDITIONAL
    return STATUS_DISCHARGED


def reconcile(raw_status: Path, schema: Path, output: Path) -> int:
    ledger = _load_toml(schema)
    policy = ledger.get("policy", {})
    allowed_statuses = set(_as_list(policy.get("allowed_statuses")))
    baseline_axioms = set(_as_list(policy.get("baseline_axioms")))
    surfaces_cfg: dict[str, Any] = ledger.get("surfaces", {})

    inventory = _parse_inventory(raw_status.read_text(encoding="utf-8"))

    errors: list[str] = []
    exported_surfaces: list[dict[str, Any]] = []

    for surface_name, cfg in sorted(surfaces_cfg.items()):
        declared_status = str(cfg.get("status", STATUS_OPEN))
        if declared_status not in allowed_statuses:
            errors.append(f"{surface_name}: invalid status {declared_status!r}")

        inv = inventory.get(
            surface_name,
            SurfaceInventory(
                name=surface_name,
                module=str(cfg.get("module", "")) or None,
                axioms=[],
                placeholders=[],
            ),
        )

        allowed_axioms = baseline_axioms | set(_as_list(cfg.get("allowed_axioms")))
        allowed_placeholders = set(_as_list(cfg.get("allowed_placeholders")))

        unregistered_axioms = sorted(set(inv.axioms) - allowed_axioms)
        unregistered_placeholders = sorted(set(inv.placeholders) - allowed_placeholders)

        if unregistered_axioms:
            errors.append(f"{surface_name}: unregistered axioms: {', '.join(unregistered_axioms)}")
        if unregistered_placeholders:
            errors.append(
                f"{surface_name}: unregistered placeholders: {', '.join(unregistered_placeholders)}"
            )

        if declared_status == STATUS_DISCHARGED and (inv.placeholders or unregistered_axioms):
            errors.append(f"{surface_name}: discharged surface has open proof boundary")

        computed_status = _surface_status(
            open_axioms=sorted(set(inv.axioms) - baseline_axioms),
            open_placeholders=inv.placeholders,
            declared_status=declared_status,
        )

        exported_surfaces.append(
            {
                "name": surface_name,
                "module": inv.module or cfg.get("module"),
                "declared_status": declared_status,
                "computed_status": computed_status,
                "axioms": inv.axioms,
                "placeholders": inv.placeholders,
                "open_assumptions": _as_list(cfg.get("open_assumptions")),
                "forbidden_promotions": _as_list(cfg.get("forbidden_promotions")),
            }
        )

    undocumented = sorted(set(inventory) - set(surfaces_cfg))
    if undocumented:
        errors.append("undocumented surfaces: " + ", ".join(undocumented))

    summary = {
        "repository": Path.cwd().name,
        "verification_boundary": {
            "total_surfaces": len(exported_surfaces),
            "discharged_surfaces": sum(
                1 for s in exported_surfaces if s["computed_status"] == STATUS_DISCHARGED
            ),
            "conditional_surfaces": sum(
                1 for s in exported_surfaces if s["computed_status"] == STATUS_CONDITIONAL
            ),
            "open_frontier_objects": sum(
                1 for s in exported_surfaces if s["computed_status"] == STATUS_OPEN
            ),
        },
        "surfaces": exported_surfaces,
        "errors": errors,
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Boundary ledger reconciled: {output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile Lean proof-boundary inventory against boundaries.toml.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    return reconcile(args.input, args.schema, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
