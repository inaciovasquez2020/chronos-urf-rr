#!/usr/bin/env python3
import json
from pathlib import Path

p = Path("docs/status/URF_FRONTIER_POINTER_REGISTRY_V1.json")
d = json.loads(p.read_text())

assert set(d.keys()) == {
    "registry_version",
    "artifact",
    "status",
    "upstream_registry",
    "upstream_canonical_source",
    "local_policy",
    "local_role",
}
print("urf-frontier-pointer-registry-schema-lock: PASS")
