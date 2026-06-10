#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/external_genuine_analytic_dini_payload_theorem1_theorem2_2026_06_09.json"
DOC = ROOT / "docs/status/EXTERNAL_GENUINE_ANALYTIC_DINI_PAYLOAD_THEOREM1_THEOREM2_2026_06_09.md"
LEAN = ROOT / "lean/Chronos/Frontier/ExternalSourceTheoremCertificateOneAxiom.lean"

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert data["object"] == "ExternalGenuineAnalyticDiniEstimatePayload_Theorem1_Theorem2"
assert data["status"] == "EXTERNAL_PAYLOAD_CERTIFICATE_ARTIFACT_ONLY"
assert data["function_ratio_source_theorem"] == "Theorem 1"
assert data["derivative_ratio_source_theorem"] == "Theorem 2"
assert data["source_equation_refs"] == ["(11)", "(12)", "(19)-(22)", "(35)-(39)"]
assert data["payload_required"] == "GenuineAnalyticDiniEstimate"
assert data["public_lean_payload_found"] is False
assert data["internal_analytic_proof_supplied"] is False
assert data["theorem_level_closure"] is False
assert data["minimal_missing_object"] == "EXTERNAL_GENUINE_ANALYTIC_DINI_ESTIMATE_PAYLOAD"

assert "Theorem 1" in lean
assert "Theorem 2" in lean
assert "source_equation_refs" in lean
assert "El_Qadeem_2022_Certificate" in lean

assert "NO_PUBLIC_LEAN_PAYLOAD" not in doc
assert "no public Lean payload" in doc
assert "no internal analytic proof" in doc
assert "no Clay claim" in doc

print("EXTERNAL_GENUINE_ANALYTIC_DINI_PAYLOAD_THEOREM1_THEOREM2_OK")
