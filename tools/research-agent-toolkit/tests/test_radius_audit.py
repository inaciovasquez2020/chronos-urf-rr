import json

import pytest

from research_agent_toolkit.radius_audit import audit_graph
from research_agent_toolkit.adaptive_radius import IncompleteAudit
from research_agent_toolkit.cli import main


def graph(edges):
    return {
        "nodes": [{"path": v} for v in ["a", "b", "c"]],
        "edges": [
            {"source": a, "target": b, "kind": "test"}
            for a, b in edges
        ],
    }


def test_dag_structural_cycle():
    result = audit_graph(graph([
        ("a", "b"), ("b", "c"), ("a", "c")
    ]))
    assert result["directed_cyclic_components"] == []
    assert result["profile"]["profile"][-1]["local_dimension"] == 1
    assert result["mutation_authorized"] is False


def test_directed_cycle():
    result = audit_graph(graph([
        ("a", "b"), ("b", "c"), ("c", "a")
    ]))
    assert result["directed_cyclic_components"] == [
        ["a", "b", "c"]
    ]


def test_self_dependency():
    result = audit_graph(graph([("a", "a")]))
    assert result["directed_cyclic_components"] == [["a"]]


def test_budget():
    with pytest.raises(IncompleteAudit):
        audit_graph(graph([("a", "b")]), max_work=1)


def test_invalid_endpoint():
    with pytest.raises(ValueError):
        audit_graph(graph([("a", "unknown")]))


def test_cli(tmp_path, capsys):
    path = tmp_path / "graph.json"
    path.write_text(json.dumps(graph([
        ("a", "b"), ("b", "c"), ("a", "c")
    ])))

    assert main(["radius-audit", str(path)]) == 0

    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "COMPLETE"
    assert result["mutation_authorized"] is False

    assert main([
        "radius-audit", str(path), "--max-work", "1"
    ]) == 2

    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "INCOMPLETE"
    assert result["mutation_authorized"] is False
