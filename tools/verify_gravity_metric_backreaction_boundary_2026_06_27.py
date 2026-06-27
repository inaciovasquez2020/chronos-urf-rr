#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("artifacts/external_validation/gravity_metric_backreaction_boundary_2026_06_27.json")
data = json.loads(path.read_text())

assert data["object"] == "GRAVITY_METRIC_BACKREACTION_BOUNDARY_2026_06_27"
assert data["repository"] == "chronos-urf-rr"
assert data["status"] == "boundary_not_solution"
assert "metric backreaction" in data["boundary"]
assert "Einstein limit" in data["boundary"]
assert "quantitative gravitational prediction" in data["boundary"]
assert "solution of gravity" in data["not_claimed"]

print("GRAVITY_METRIC_BACKREACTION_BOUNDARY_2026_06_27_OK")
