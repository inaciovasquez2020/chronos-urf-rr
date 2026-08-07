from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent_mutation import governed_patch_mutation
from .budgets import Budget
from .calendar_export import export_ics
from .engine import evaluate, load_config
from .finetune_manifest import prepare_jsonl
from .index import index_file, search
from .lean_exact import exact_lean_dependencies, reverse_declaration_closure
from .profile import build_profile
from .provenance import build_provenance, load_manifest
from .scanner import scan, reverse_closure
from .server import serve_stdio


def _json(obj) -> None:
    print(json.dumps(obj, indent=2, sort_keys=True, default=lambda x: x.__dict__))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="rat")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan")
    s.add_argument("root")
    s.add_argument("--out")

    ld = sub.add_parser("lean-deps")
    ld.add_argument("root")
    ld.add_argument("modules", nargs="+")
    ld.add_argument("--out")

    ldc = sub.add_parser("lean-closure")
    ldc.add_argument("root")
    ldc.add_argument("--module", dest="modules", action="append", required=True)
    ldc.add_argument("changed", nargs="+")

    pv = sub.add_parser("provenance")
    pv.add_argument("root")
    pv.add_argument("manifest")
    pv.add_argument("modules", nargs="+")
    pv.add_argument("--out")

    mut = sub.add_parser("mutate")
    mut.add_argument("root")
    mut.add_argument("manifest")
    mut.add_argument("changed")
    mut.add_argument("--patch", required=True)
    mut.add_argument("--verifier-json", required=True)
    mut.add_argument(
        "--module",
        dest="modules",
        action="append",
        default=[],
    )

    c = sub.add_parser("closure")
    c.add_argument("root")
    c.add_argument("changed", nargs="+")

    g = sub.add_parser("gate")
    g.add_argument("--config", required=True)
    g.add_argument("--action", required=True)
    g.add_argument("--paths", nargs="+", required=True)
    g.add_argument("--candidate")

    i = sub.add_parser("index")
    i.add_argument("--db", required=True)
    i.add_argument("files", nargs="+")

    q = sub.add_parser("search")
    q.add_argument("--db", required=True)
    q.add_argument("query")
    q.add_argument("--limit", type=int, default=5)

    pr = sub.add_parser("profile")
    pr.add_argument("traces", nargs="+")

    ft = sub.add_parser("prepare-finetune")
    ft.add_argument("input")
    ft.add_argument("output")

    srv = sub.add_parser("serve")
    srv.add_argument("--root", required=True)
    srv.add_argument("--config", required=True)
    srv.add_argument("--db", required=True)

    cal = sub.add_parser("calendar")
    cal.add_argument("events_json")
    cal.add_argument("output_ics")

    args = p.parse_args(argv)
    if args.cmd == "scan":
        graph = scan(args.root)
        if args.out:
            graph.write(Path(args.out))
        _json(graph.to_dict())
        return 0
    if args.cmd == "lean-deps":
        graph = exact_lean_dependencies(args.root, args.modules)
        data = graph.to_dict()
        if args.out:
            Path(args.out).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        _json(data)
        return 0
    if args.cmd == "lean-closure":
        graph = exact_lean_dependencies(args.root, args.modules)
        _json(reverse_declaration_closure(graph, args.changed))
        return 0
    if args.cmd == "provenance":
        lean_graph = exact_lean_dependencies(args.root, args.modules)
        graph = build_provenance(args.root, load_manifest(args.manifest), lean_graph)
        data = graph.to_dict()
        if args.out:
            Path(args.out).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        _json(data)
        return 0
    if args.cmd == "mutate":
        verifier = json.loads(
            args.verifier_json
        )

        if (
            not isinstance(verifier, list)
            or not verifier
            or not all(
                isinstance(item, str) and item
                for item in verifier
            )
        ):
            raise SystemExit(
                "verifier JSON must be a nonempty "
                "array of nonempty strings"
            )

        patch = Path(
            args.patch
        ).read_text(
            encoding="utf-8"
        )

        result = governed_patch_mutation(
            args.root,
            args.manifest,
            args.changed,
            patch,
            verifier,
            modules=args.modules,
        )

        _json(result)

        if result.preserved:
            return 0

        return result.returncode or 1

    if args.cmd == "closure":
        _json(reverse_closure(scan(args.root), args.changed))
        return 0
    if args.cmd == "gate":
        cfg = load_config(args.config)
        candidate = Path(args.candidate).read_text() if args.candidate else None
        budget = Budget(cfg.get("budgets", {}))
        decision = evaluate(cfg, args.action, args.paths, candidate, budget)
        _json(decision)
        return 0 if decision.status != "DENY" else 2
    if args.cmd == "index":
        result = {str(f): index_file(args.db, f) for f in args.files}
        _json(result)
        return 0
    if args.cmd == "search":
        _json(search(args.db, args.query, args.limit))
        return 0
    if args.cmd == "profile":
        _json(build_profile(args.traces))
        return 0
    if args.cmd == "prepare-finetune":
        _json(prepare_jsonl(args.input, args.output))
        return 0
    if args.cmd == "serve":
        return serve_stdio(root=args.root, config=args.config, db=args.db)
    if args.cmd == "calendar":
        events = json.loads(Path(args.events_json).read_text())
        export_ics(events, args.output_ics)
        return 0
    raise AssertionError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())
