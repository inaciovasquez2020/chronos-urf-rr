from pathlib import Path
import json

lean_path = Path("lean/Chronos/Frontier/MeaningfulExternalH41FGLToyClosure.lean")
status_path = Path("docs/status/MEANINGFUL_EXTERNAL_H41FGL_TOY_CLOSURE_2026_05_16.md")
artifact_path = Path("artifacts/chronos/meaningful_external_h41fgl_toy_closure_2026_05_16.json")

lean = lean_path.read_text()
status = status_path.read_text()
artifact = json.loads(artifact_path.read_text())

required_lean = [
    "structure Witness",
    "structure CountingFiberSeparationFromNonProp",
    "def extract_witness_from_counting_fiber_separation",
    "theorem counting_implies_nonempty",
    "def NonPropFinalCarrierInvariant",
    "def UniversalFiberEntropyGap",
    "def ChronosRR",
    "def H41FGL",
    "structure ExternalH41FGLModel",
    "structure NonRepackagedExternalH41FGLModel",
    "structure MeaningfulExternalH41FGLModel",
    "theorem bool_not_injects_witness",
    "def build_meaningful_external_h41_fgl_model",
    "theorem counting_implies_meaningful_external_intended_h41_fgl",
    "theorem impossible_external_preservation_refuted",
]

for phrase in required_lean:
    assert phrase in lean, phrase

required_status = [
    "VERIFIED_TOY_EXTERNAL_MODEL_ONLY",
    "toy external-model closure",
    "does not prove a nontrivial external H4.1/FGL theorem",
    "does not prove unrestricted Chronos-RR",
    "does not prove unrestricted H4.1/FGL",
    "does not prove P vs NP",
    "does not solve any Clay problem",
]

for phrase in required_status:
    assert phrase in status, phrase

assert artifact["status"] == "VERIFIED_TOY_EXTERNAL_MODEL_ONLY"
assert artifact["lean_module"] == "Chronos.Frontier.MeaningfulExternalH41FGLToyClosure"

for theorem in [
    "counting_implies_nonempty",
    "counting_implies_h41_fgl",
    "build_meaningful_external_h41_fgl_model",
    "counting_implies_meaningful_external_intended_h41_fgl",
]:
    assert theorem in artifact["proved"], theorem

combined = "\n".join([lean, status, json.dumps(artifact)]).lower()

for forbidden in [
    "solves p vs np",
    "proves p vs np",
    "solves any clay problem",
    "proves any clay problem",
    "proves a nontrivial external h4.1/fgl theorem",
    "proves unrestricted chronos-rr",
    "proves unrestricted h4.1/fgl",
]:
    assert forbidden not in combined, forbidden

print("Meaningful external H41FGL toy closure verified.")
