#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/chronos/global_urf_decision_audit_2026_05_18.json"
OUT = ROOT / "artifacts/chronos/global_urf_decision_audit_dependency_dag_2026_05_18.json"
DOC = ROOT / "docs/status/GLOBAL_URF_DECISION_AUDIT_DEPENDENCY_DAG_2026_05_18.md"

def main() -> None:
    source = json.loads(SOURCE.read_text())
    claims = source["claims"]

    nodes = []
    edges = []

    for claim in claims:
        claim_id = claim["id"]
        a_node = f"A:{claim_id}"
        b_node = f"B:{claim_id}"
        proof_node = f"ProofTarget:{claim_id}"
        counter_node = f"CountermodelTarget:{claim_id}"
        sink_node = f"Sink:{claim['sink_lemma']}"

        nodes.extend([
            {"id": a_node, "kind": "assumption", "label": claim["A_i"]},
            {"id": b_node, "kind": "conclusion", "label": claim["B_i"]},
            {"id": proof_node, "kind": "lean_proof_target", "label": claim["lean_proof_target"]},
            {"id": counter_node, "kind": "countermodel_target", "label": claim["countermodel_target"]},
            {"id": sink_node, "kind": "sink_lemma", "label": claim["sink_lemma"]},
        ])

        edges.extend([
            {"source": a_node, "target": b_node, "relation": "normalized_implication"},
            {"source": proof_node, "target": b_node, "relation": "attempts_to_verify"},
            {"source": counter_node, "target": b_node, "relation": "attempts_to_refute"},
            {"source": sink_node, "target": b_node, "relation": "blocks_or_closes"},
        ])

    unique_nodes = {node["id"]: node for node in nodes}
    sink_nodes = sorted(
        node["id"] for node in unique_nodes.values()
        if node["kind"] == "sink_lemma" and node["label"] != "none"
    )

    dag = {
        "artifact": "global_urf_decision_audit_dependency_dag",
        "date": "2026-05-18",
        "status": "DAG_SURFACE_ONLY",
        "source_artifact": "global_urf_decision_audit_2026_05_18.json",
        "global_verdict": source["global_verdict"],
        "node_count": len(unique_nodes),
        "edge_count": len(edges),
        "sink_node_count": len(sink_nodes),
        "nodes": list(unique_nodes.values()),
        "edges": edges,
        "sink_nodes": sink_nodes,
        "boundary": [
            "Dependency DAG only.",
            "Does not prove unrestricted UniversalFiberEntropyGap.",
            "Does not prove unrestricted Chronos-RR.",
            "Does not prove unrestricted H4.1/FGL.",
            "Does not prove P vs NP.",
            "Does not prove any Clay problem."
        ],
    }

    OUT.write_text(json.dumps(dag, indent=2, sort_keys=True) + "\n")

    DOC.write_text(
        "# Global URF Decision Audit Dependency DAG\n\n"
        "Status: `DAG_SURFACE_ONLY`\n\n"
        "Source artifact: `global_urf_decision_audit_2026_05_18.json`\n\n"
        f"Global verdict: `{dag['global_verdict']}`\n\n"
        "## Numeric graph values\n\n"
        f"- Node count: `{dag['node_count']}`\n"
        f"- Edge count: `{dag['edge_count']}`\n"
        f"- Sink node count: `{dag['sink_node_count']}`\n\n"
        "## Sink nodes\n\n"
        + "\n".join(f"- `{node}`" for node in dag["sink_nodes"])
        + "\n\n## Boundary\n\n"
        "Dependency DAG only.\n\n"
        "Does not prove:\n\n"
        "- unrestricted `UniversalFiberEntropyGap`\n"
        "- unrestricted Chronos-RR\n"
        "- unrestricted H4.1/FGL\n"
        "- P vs NP\n"
        "- any Clay problem\n"
    )

if __name__ == "__main__":
    main()
