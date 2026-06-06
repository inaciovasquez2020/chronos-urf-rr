#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("artifacts/chronos/main_ci_independent_audit_gate_2026_06_06.json")
data = json.loads(path.read_text())

assert data["artifact"] == "MAIN_CI_INDEPENDENT_AUDIT_GATE_2026_06_06"
assert data["status"] == "AUDIT_BACKED_GATE_RECORDED_ONLY"
assert data["claims"]["adds_verification_gate"] is True
assert data["claims"]["asserts_new_theorem"] is False
assert data["claims"]["asserts_chronos_rr_closure"] is False
assert data["claims"]["asserts_h41_fgl_closure"] is False
assert data["claims"]["asserts_p_vs_np_closure"] is False
assert data["claims"]["asserts_clay_problem_closure"] is False

ci = data["latest_main_ci"]
audit = data["latest_independent_audit"]

assert ci is not None
assert audit is not None
assert ci["status"] == "completed"
assert ci["conclusion"] == "success"
assert audit["status"] == "completed"
assert audit["conclusion"] == "success"

print("MAIN_CI_INDEPENDENT_AUDIT_GATE_OK")
