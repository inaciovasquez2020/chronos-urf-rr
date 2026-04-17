#!/usr/bin/env python3
import json
from pathlib import Path

pointer = Path("docs/status/URF_FRONTIER_POINTER_REGISTRY_V1.json")
doc = Path("docs/status/WHOLE_URF_FRONTIER_POINTER.md")

d = json.loads(pointer.read_text())
s = doc.read_text()

assert d["registry_version"] == 1
assert d["status"] == "POINTER_ONLY"
assert d["local_policy"] == "no_status_escalation"
assert d["local_role"] == "downstream_pointer"
assert "URF_FRONTIER_REGISTRY_V1.json" in d["upstream_registry"]
assert "URF_REMAINING_FRONTIER_CANONICAL.md" in d["upstream_canonical_source"]

assert "does not define whole-URF residual frontier status" in s
assert "Canonical pointer:" in s
assert "URF_REMAINING_FRONTIER_CANONICAL.md" in s

print("projection-check: PASS")
