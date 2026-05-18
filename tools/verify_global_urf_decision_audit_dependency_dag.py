#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAG = ROOT / "artifacts/chronos/global_urf_decision_audit_dependency_dag_2026_05_18.json"
DOC = ROOT / "docs/status/GLOBAL_URF_DECISION_AUDIT_DEPENDENCY_DAG_2026_05_18.md"

def main() -> None:
    data = json.loads(DAG.read_text())
    doc = DOC.read_text()

    assert data["artifact"] == "global_urf_decision_audit_dependency_dag"
    assert data["status"] == "DAG_SURFACE_ONLY"
    assert data["global_verdict"] == "OPEN_WITH_EXPLICIT_SINK_LEMMAS"

    assert data["node_count"] >= 17
    assert data["edge_count"] == 16
    assert data["sink_node_count"] == 3

    node_ids = {node["id"] for node in data["nodes"]}
    assert "Sink:unrestricted uniform positivity/coercivity" in node_ids
    assert "Sink:unrestricted UniversalFiberEntropyGap plus unrestricted DepthBridge" in node_ids
    assert "B:unrestricted_universal_fiber_entropy_gap" in node_ids
    assert "B:unrestricted_chronos_rr_h41_fgl_p_np_clay" in node_ids

    relations = {edge["relation"] for edge in data["edges"]}
    assert "normalized_implication" in relations
    assert "attempts_to_verify" in relations
    assert "attempts_to_refute" in relations
    assert "blocks_or_closes" in relations

    assert "DAG_SURFACE_ONLY" in doc
    assert "Dependency DAG only." in doc
    assert "Does not prove:" in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc

    forbidden = [
        "proves unrestricted UniversalFiberEntropyGap",
        "proves unrestricted Chronos-RR",
        "proves unrestricted H4.1/FGL",
        "proves P vs NP",
        "proves any Clay problem",
        "Clay problem solved",
    ]
    for token in forbidden:
        assert token not in doc

    print("Global URF decision audit dependency DAG verified.")

if __name__ == "__main__":
    main()
