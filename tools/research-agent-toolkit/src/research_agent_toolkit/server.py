from __future__ import annotations

import json
import sys
from pathlib import Path

from .budgets import Budget
from .engine import evaluate, load_config
from .index import search
from .lean_exact import exact_lean_dependencies
from .provenance import build_provenance, load_manifest
from .scanner import reverse_closure, scan


def tool_definitions() -> list[dict]:
    return [
        {"name": "scan", "description": "Scan the configured repository dependency graph.", "inputSchema": {"type": "object", "properties": {}}},
        {"name": "closure", "description": "Compute reverse file dependency closure.", "inputSchema": {"type": "object", "properties": {"changed": {"type": "array", "items": {"type": "string"}}}, "required": ["changed"]}},
        {"name": "lean_deps", "description": "Compute exact Lean declaration dependencies from elaborated modules.", "inputSchema": {"type": "object", "properties": {"modules": {"type": "array", "items": {"type": "string"}}}, "required": ["modules"]}},
        {"name": "gate", "description": "Evaluate scope, policy, budget, and approval gate rules.", "inputSchema": {"type": "object", "properties": {"action": {"type": "string"}, "paths": {"type": "array", "items": {"type": "string"}}, "candidate": {"type": ["string", "null"]}}, "required": ["action", "paths"]}},
        {"name": "search", "description": "Search the configured local research index.", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["query"]}},
        {"name": "provenance", "description": "Build theorem/claim to generator to artifact to test provenance edges.", "inputSchema": {"type": "object", "properties": {"manifest": {"type": "string"}, "modules": {"type": "array", "items": {"type": "string"}}}, "required": ["manifest"]}},
    ]


def _content(value) -> dict:
    return {"content": [{"type": "text", "text": json.dumps(value, sort_keys=True, default=lambda x: x.__dict__)}]}


def handle_request(request: dict, *, root: str | Path, config: str | Path, db: str | Path) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    try:
        if method == "initialize":
            result = {"serverInfo": {"name": "research-agent-toolkit", "version": "0.2.0"}, "capabilities": {"tools": {}}}
        elif method == "tools/list":
            result = {"tools": tool_definitions()}
        elif method == "tools/call":
            params = request.get("params") or {}
            name = params.get("name")
            args = params.get("arguments") or {}
            if name == "scan":
                result = _content(scan(root).to_dict())
            elif name == "closure":
                result = _content(reverse_closure(scan(root), list(args["changed"])))
            elif name == "lean_deps":
                result = _content(exact_lean_dependencies(root, list(args["modules"])).to_dict())
            elif name == "gate":
                cfg = load_config(config)
                decision = evaluate(cfg, str(args["action"]), list(args["paths"]), args.get("candidate"), Budget(cfg.get("budgets", {})))
                result = _content(decision)
            elif name == "search":
                result = _content(search(db, str(args["query"]), int(args.get("limit", 5))))
            elif name == "provenance":
                manifest_path = (Path(root) / str(args["manifest"])).resolve()
                manifest_path.relative_to(Path(root).resolve())
                modules = list(args.get("modules") or [])
                lean_graph = (
                    exact_lean_dependencies(root, modules)
                    if modules
                    else None
                )
                result = _content(
                    build_provenance(
                        root,
                        load_manifest(manifest_path),
                        lean_graph,
                    ).to_dict()
                )
            else:
                raise ValueError(f"unknown tool: {name}")
        else:
            raise ValueError(f"unknown method: {method}")
        return {"jsonrpc": "2.0", "id": req_id, "result": result}
    except Exception as exc:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(exc)}}


def serve_stdio(*, root: str | Path, config: str | Path, db: str | Path) -> int:
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            request = json.loads(raw)
        except json.JSONDecodeError as exc:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}
        else:
            response = handle_request(request, root=root, config=config, db=db)
        sys.stdout.write(json.dumps(response, separators=(",", ":")) + "\n")
        sys.stdout.flush()
    return 0
