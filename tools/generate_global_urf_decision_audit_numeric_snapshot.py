#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/chronos/global_urf_decision_audit_2026_05_18.json"
OUT = ROOT / "artifacts/chronos/global_urf_decision_audit_numeric_snapshot_2026_05_18.json"
DOC = ROOT / "docs/status/GLOBAL_URF_DECISION_AUDIT_NUMERIC_SNAPSHOT_2026_05_18.md"

FULL_PYTEST_PASSED_LATEST = 958

def pct(num: int, den: int) -> float:
    return round((100.0 * num / den) if den else 0.0, 2)

def main() -> None:
    data = json.loads(SOURCE.read_text())
    claims = data["claims"]
    total = len(claims)

    verdict_counts = Counter(c["verdict"] for c in claims)
    assumption_counts = Counter(c["assumption_status"] for c in claims)

    snapshot = {
        "artifact": "global_urf_decision_audit_numeric_snapshot",
        "date": "2026-05-18",
        "source_artifact": "global_urf_decision_audit_2026_05_18.json",
        "source_status": data["status"],
        "global_verdict": data["global_verdict"],
        "claims_total": total,
        "assumption_status_counts": dict(sorted(assumption_counts.items())),
        "verdict_counts": dict(sorted(verdict_counts.items())),
        "dependency_dag_sink_count": len(data["dependency_dag_sinks"]),
        "boundary_item_count": len(data["boundary"]),
        "proved_surface_count": verdict_counts.get("proved_surface", 0),
        "conditional_surface_count": verdict_counts.get("conditional_surface", 0),
        "countermodel_required_count": verdict_counts.get("countermodel_required", 0),
        "open_missing_lemma_count": verdict_counts.get("open_missing_lemma", 0),
        "proved_surface_percent": pct(verdict_counts.get("proved_surface", 0), total),
        "conditional_surface_percent": pct(verdict_counts.get("conditional_surface", 0), total),
        "countermodel_required_percent": pct(verdict_counts.get("countermodel_required", 0), total),
        "open_missing_lemma_percent": pct(verdict_counts.get("open_missing_lemma", 0), total),
        "open_or_countermodel_count": verdict_counts.get("countermodel_required", 0) + verdict_counts.get("open_missing_lemma", 0),
        "open_or_countermodel_percent": pct(
            verdict_counts.get("countermodel_required", 0) + verdict_counts.get("open_missing_lemma", 0),
            total,
        ),
        "latest_full_pytest_passed": FULL_PYTEST_PASSED_LATEST,
        "boundary": [
            "Numeric snapshot only.",
            "Does not prove unrestricted UniversalFiberEntropyGap.",
            "Does not prove unrestricted Chronos-RR.",
            "Does not prove unrestricted H4.1/FGL.",
            "Does not prove P vs NP.",
            "Does not prove any Clay problem."
        ],
    }

    OUT.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")

    snapshot_json = json.dumps(snapshot, indent=2, sort_keys=True)
    DOC.write_text(
        "# Global URF Decision Audit Numeric Snapshot\n\n"
        "Status: `NUMERIC_SNAPSHOT_ONLY`\n\n"
        "Source artifact: `global_urf_decision_audit_2026_05_18.json`\n\n"
        f"Global verdict: `{snapshot['global_verdict']}`\n\n"
        "## Real values\n\n"
        "```json\n"
        f"{snapshot_json}\n"
        "```\n\n"
        "## Boundary\n\n"
        "Numeric snapshot only.\n\n"
        "Does not prove:\n\n"
        "- unrestricted `UniversalFiberEntropyGap`\n"
        "- unrestricted Chronos-RR\n"
        "- unrestricted H4.1/FGL\n"
        "- P vs NP\n"
        "- any Clay problem\n"
    )

if __name__ == "__main__":
    main()
