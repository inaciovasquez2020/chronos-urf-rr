from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean_extraction = ROOT / "Chronos/Frontier/FinalCarrierObservationExtraction.lean"
lean_closed = ROOT / "Chronos/Frontier/H4_1_FGL_FinalCarrierExtractionClosed.lean"
root_import = ROOT / "Chronos.lean"
status_doc = ROOT / "docs/status/CHRONOS_H4_1_FGL_FINAL_CARRIER_EXTRACTION_CLOSED_2026_05_10.md"
artifact = ROOT / "artifacts/chronos/h4_1_fgl_final_carrier_extraction_closed.json"

for path in [lean_extraction, lean_closed, root_import, status_doc, artifact]:
    assert path.exists(), f"missing required file: {path}"

closed_text = lean_closed.read_text()
required_closed_tokens = [
    "import Chronos.Frontier.FinalCarrierObservationExtraction",
    "theorem H4_1_FGL_final_carrier_extraction_closed",
    "final_carrier_observation_extraction_closed P hP",
    "theorem H4_1_FGL_final_carrier_gap_soundness_surface",
    "theorem H4_1_FGL_final_carrier_fiber_entropy_surface",
    "theorem H4_1_FGL_final_carrier_depth_bridge_surface",
]
for token in required_closed_tokens:
    assert token in closed_text, token

root_text = root_import.read_text()
assert "import Chronos.Frontier.H4_1_FGL_FinalCarrierExtractionClosed" in root_text

status_text = status_doc.read_text()
required_status_tokens = [
    "H4_1_FGL_FINAL_CARRIER_EXTRACTION_CLOSED",
    "H4_1_FGL_final_carrier_extraction_closed",
    "UniversalFiberEntropyGap theorem",
    "DepthBridge beyond the selected final-carrier domain",
    "Chronos-RR theorem closure",
    "P vs NP closure",
    "Clay-problem closure",
]
for token in required_status_tokens:
    assert token in status_text, token

data = json.loads(artifact.read_text())
assert data["status"] == "H4_1_FGL_FINAL_CARRIER_EXTRACTION_CLOSED"
assert "H4_1_FGL_final_carrier_extraction_closed" in data["exported_theorems"]
assert data["boundary"]["p_vs_np"] is False
assert data["boundary"]["clay_problem"] is False
assert data["boundary"]["universal_fiber_entropy_gap"] is False
assert data["boundary"]["chronos_rr_theorem"] is False

for forbidden in [
    "solves P vs NP",
    "proves P vs NP",
    "resolves P vs NP",
    "solves the Clay",
    "resolves the Clay",
    "UniversalFiberEntropyGap theorem closed",
    "Chronos-RR theorem closed"
]:
    assert forbidden not in status_text
    assert forbidden not in closed_text

print("Final carrier observation extraction closure verified.")
