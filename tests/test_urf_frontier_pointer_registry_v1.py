import json
from pathlib import Path

def test_urf_frontier_pointer_registry_v1():
    p = Path("docs/status/URF_FRONTIER_POINTER_REGISTRY_V1.json")
    d = json.loads(p.read_text())
    assert d["registry_version"] == 1
    assert d["artifact"] == "URF_FRONTIER_POINTER_REGISTRY_V1"
    assert d["status"] == "POINTER_ONLY"
    assert d["local_policy"] == "no_status_escalation"
    assert d["local_role"] == "downstream_pointer"
    assert "URF_FRONTIER_REGISTRY_V1.json" in d["upstream_registry"]
    assert "URF_REMAINING_FRONTIER_CANONICAL.md" in d["upstream_canonical_source"]
