from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_cpdl_ccsl_conditional_gate_artifact():
    data = json.loads((ROOT / "artifacts/chronos/cpdl_ccsl_conditional_gate.json").read_text())
    assert data["status"] == "CONDITIONAL_GATE_ONLY"
    assert data["theorem_closure"] is False
    assert data["chronos_certificate_embedding"] is False
    assert data["h41_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False

def test_cpdl_ccsl_conditional_gate_boundary_doc():
    text = (ROOT / "docs/status/CHRONOS_CPDL_CCSL_CONDITIONAL_GATE_2026_05_04.md").read_text()
    assert "MissingCPDLCCSLWitness" in text
    assert "does not construct" in text
    assert "does not define" in text
    assert "does not prove ChronosCertificateEmbedding" in text
    assert "does not prove H4.1/FGL theorem closure" in text
    assert "does not prove P vs NP closure" in text

def test_cpdl_ccsl_lean_surface():
    text = (ROOT / "Chronos/CPDLCCSLGate.lean").read_text()
    assert "structure CPDLGate" in text
    assert "structure CCSLGate" in text
    assert "def MissingCPDLCCSLWitness" in text
    assert "theorem cpdl_validity_of_ccsl_embedding" in text
    assert "theorem ccsl_injective" in text
