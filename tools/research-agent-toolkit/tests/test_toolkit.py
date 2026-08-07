import json
from pathlib import Path

from research_agent_toolkit.budgets import Budget, BudgetExceeded
from research_agent_toolkit.engine import evaluate
from research_agent_toolkit.index import index_file, search
from research_agent_toolkit.scanner import scan, reverse_closure


def test_scanner_and_reverse_closure(tmp_path: Path):
    (tmp_path / "a.py").write_text("import b\ndef f(): return 1\n")
    (tmp_path / "b.py").write_text("def g(): return 2\n")
    graph = scan(tmp_path)
    assert any(e.source == "a.py" and e.target == "b.py" for e in graph.edges)
    assert reverse_closure(graph, ["b.py"]) == ["a.py", "b.py"]


def test_policy_and_scope():
    cfg = {
        "scope": {"allow": ["src/**"], "deny": ["src/vendor/**"]},
        "policy": {"forbidden_patterns": [r"\bsorry\b"]},
        "gates": {"verify_actions": ["modify"], "deny_actions": []},
    }
    assert evaluate(cfg, "modify", ["src/x.lean"], "theorem x : True := by trivial").status == "VERIFY"
    assert evaluate(cfg, "modify", ["src/x.lean"], "theorem x : True := by sorry").status == "DENY"
    assert evaluate(cfg, "modify", ["other/x.lean"], "ok").status == "DENY"


def test_budget():
    b = Budget({"mutations": 1})
    b.consume("mutations")
    try:
        b.consume("mutations")
    except BudgetExceeded:
        pass
    else:
        raise AssertionError("budget should fail")


def test_local_index(tmp_path: Path):
    f = tmp_path / "note.md"
    f.write_text("interval Newton certifies a unique simple root in the matching box")
    db = tmp_path / "idx.db"
    assert index_file(db, f) == 1
    rows = search(db, "unique root interval Newton")
    assert rows and rows[0]["source"] == str(f)


def test_verified_mutation_reverts_first_failure(tmp_path: Path):
    from research_agent_toolkit.transaction import verified_mutation

    target = tmp_path / "x.txt"
    target.write_text("before")

    def mutate():
        target.write_text("after")

    result = verified_mutation(
        [target],
        mutate,
        ["python3", "-c", "raise SystemExit(7)"],
        cwd=tmp_path,
    )
    assert not result.preserved
    assert result.returncode == 7
    assert target.read_text() == "before"


def test_exact_lean_probe_parser_and_reverse_closure():
    from research_agent_toolkit.lean_exact import parse_probe_output, reverse_declaration_closure

    graph = parse_probe_output(
        "\n".join(
            [
                "RAT_DECL\tFoo\tthm\tFoo.base",
                "RAT_DECL\tFoo\tthm\tFoo.step",
                "RAT_EDGE\tFoo.step\tFoo.base",
                "RAT_EDGE\tFoo.step\tNat.succ",
            ]
        ),
        ["Foo"],
    )
    assert [d.name for d in graph.declarations] == ["Foo.base", "Foo.step"]
    assert reverse_declaration_closure(graph, ["Foo.base"]) == ["Foo.base", "Foo.step"]


def test_provenance_chain(tmp_path: Path):
    from research_agent_toolkit.lean_exact import LeanDeclaration, LeanExactGraph
    from research_agent_toolkit.provenance import build_provenance, forward_closure

    for rel in ["gen.py", "artifact.json", "test_result.py"]:
        (tmp_path / rel).write_text("x")
    lean = LeanExactGraph(["Foo"], [LeanDeclaration("Foo.thm", "Foo", "thm")], [])
    graph = build_provenance(
        tmp_path,
        {"chains": [{"theorem": "Foo.thm", "generator": "gen.py", "artifact": "artifact.json", "test": "test_result.py"}]},
        lean,
    )
    assert [(e.source, e.target, e.kind) for e in graph.edges] == [
        ("Foo.thm", "gen.py", "theorem_to_generator"),
        ("artifact.json", "test_result.py", "artifact_to_test"),
        ("gen.py", "artifact.json", "generator_to_artifact"),
    ]
    assert forward_closure(graph, ["Foo.thm"]) == ["Foo.thm", "artifact.json", "gen.py", "test_result.py"]


def test_dependency_transaction_reverts_verifier_failure(tmp_path: Path):
    import subprocess
    from research_agent_toolkit.transaction import verified_dependency_subprocess

    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "rat@example.invalid"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "RAT Test"], cwd=tmp_path, check=True)
    target = tmp_path / "x.txt"
    target.write_text("before\n")
    subprocess.run(["git", "add", "x.txt"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=tmp_path, check=True)

    result = verified_dependency_subprocess(
        tmp_path,
        ["x.txt"],
        ["python3", "-c", "from pathlib import Path; Path('x.txt').write_text('after\\n')"],
        ["python3", "-c", "raise SystemExit(7)"],
    )
    assert not result.preserved
    assert result.phase == "verification"
    assert result.returncode == 7
    assert target.read_text() == "before\n"
    assert subprocess.run(["git", "status", "--porcelain"], cwd=tmp_path, text=True, capture_output=True).stdout == ""


def test_tool_server_scan_gate_search(tmp_path: Path):
    from research_agent_toolkit.index import index_file
    from research_agent_toolkit.server import handle_request

    (tmp_path / "a.py").write_text("def f(): return 1\n")
    config = tmp_path / "toolkit.json"
    config.write_text(json.dumps({"scope": {"allow": ["*.py"], "deny": []}, "gates": {"verify_actions": ["modify"], "deny_actions": []}, "policy": {"forbidden_patterns": []}, "budgets": {"mutations": 1}}))
    db = tmp_path / "research.db"
    note = tmp_path / "note.md"
    note.write_text("exact declaration dependency graph")
    index_file(db, note)

    scan_response = handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "scan", "arguments": {}}}, root=tmp_path, config=config, db=db)
    assert "error" not in scan_response
    gate_response = handle_request({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "gate", "arguments": {"action": "modify", "paths": ["a.py"], "candidate": "ok"}}}, root=tmp_path, config=config, db=db)
    assert "VERIFY" in gate_response["result"]["content"][0]["text"]
    search_response = handle_request({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search", "arguments": {"query": "dependency graph"}}}, root=tmp_path, config=config, db=db)
    assert "note.md" in search_response["result"]["content"][0]["text"]


def test_provenance_claim_chain(tmp_path: Path):
    from research_agent_toolkit.provenance import (
        build_provenance,
        forward_closure,
    )

    for rel in [
        "gen.py",
        "artifact.json",
        "test_result.py",
    ]:
        (tmp_path / rel).write_text("x")

    claim = "gfe.axial.220.projected_eft.claim"

    graph = build_provenance(
        tmp_path,
        {
            "chains": [
                {
                    "claim": claim,
                    "generator": "gen.py",
                    "artifact": "artifact.json",
                    "test": "test_result.py",
                }
            ]
        },
    )

    assert {
        (edge.source, edge.target, edge.kind)
        for edge in graph.edges
    } == {
        (
            claim,
            "gen.py",
            "claim_to_generator",
        ),
        (
            "gen.py",
            "artifact.json",
            "generator_to_artifact",
        ),
        (
            "artifact.json",
            "test_result.py",
            "artifact_to_test",
        ),
    }

    assert forward_closure(
        graph,
        [claim],
    ) == [
        "artifact.json",
        "gen.py",
        claim,
        "test_result.py",
    ]
