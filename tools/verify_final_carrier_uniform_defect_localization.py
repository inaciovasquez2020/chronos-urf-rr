from pathlib import Path
import json
DOC = Path("docs/status/CHRONOS_FINAL_CARRIER_UNIFORM_DEFECT_LOCALIZATION_2026_05_10.md")
ARTIFACT = Path("artifacts/chronos/final_carrier_uniform_defect_localization_2026_05_10.json")
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())
required_doc_tokens = [
"FRONTIER_EXACTLY_LOCALIZED",
"FinalCarrierDomainNormalForm",
"FinalCarrierDomainUniformArityBound",
"UniformStratumDefect",
"∃ B : ℕ, ∀ c : ChronosCarrierData",
"FinalCarrierDomain c → c.arity ≤ B",
"It does not prove `FinalCarrierDomainUniformArityBound`.",
"It does not prove `FinalCarrierDomainNormalForm → UniformStratumDefect`.",
"It does not prove unrestricted Chronos-RR.",
"It does not prove H4.1/FGL.",
"It does not prove UniversalFiberEntropyGap.",
"It does not prove P vs NP or any Clay-problem result.",
]
for token in required_doc_tokens:
    assert token in doc, token
assert artifact["status"] == "FRONTIER_EXACTLY_LOCALIZED"
assert artifact["weakest_missing_theorem_level_input"] == "FinalCarrierDomainUniformArityBound"
assert "FinalCarrierDomainNormalForm -> UniformStratumDefect" in artifact["not_established"]
assert "does_not_prove_FinalCarrierDomainUniformArityBound" in artifact["boundary"]
assert "does_not_prove_FinalCarrierDomainNormalForm_to_UniformStratumDefect" in artifact["boundary"]
assert "does_not_prove_P_vs_NP_or_Clay" in artifact["boundary"]
combined = doc + json.dumps(artifact)
forbidden_tokens = [
"FinalCarrierDomainUniformArityBound is proved",
"FinalCarrierDomainNormalForm implies UniformStratumDefect",
"unrestricted Chronos-RR is proved",
"H4.1/FGL is proved",
"UniversalFiberEntropyGap is proved",
"P vs NP is proved",
"Clay problem solved",
]
for token in forbidden_tokens:
    assert token not in combined, token
print("FinalCarrierUniformDefect localization verified: FRONTIER_EXACTLY_LOCALIZED")
