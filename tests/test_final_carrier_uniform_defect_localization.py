from pathlib import Path
import json

DOC = Path("docs/status/CHRONOS_FINAL_CARRIER_UNIFORM_DEFECT_LOCALIZATION_2026_05_10.md")
ARTIFACT = Path("artifacts/chronos/final_carrier_uniform_defect_localization_2026_05_10.json")


def test_status_and_missing_input_are_recorded():
    doc = DOC.read_text()
    artifact = json.loads(ARTIFACT.read_text())

    assert "FRONTIER_EXACTLY_LOCALIZED" in doc
    assert artifact["status"] == "FRONTIER_EXACTLY_LOCALIZED"
    assert artifact["weakest_missing_theorem_level_input"] == "FinalCarrierDomainUniformArityBound"


def test_conditional_chain_is_not_promoted():
    doc = DOC.read_text()

    assert "FinalCarrierDomainNormalForm →" in doc
    assert "FinalCarrierDomainUniformArityBound →" in doc
    assert "UniformStratumDefect" in doc
    assert "It does not prove `FinalCarrierDomainNormalForm → UniformStratumDefect`." in doc
    assert "It does not prove `FinalCarrierDomainUniformArityBound`." in doc


def test_boundary_guards_remain_explicit():
    doc = DOC.read_text()

    required = [
        "It does not prove unrestricted Chronos-RR.",
        "It does not prove H4.1/FGL.",
        "It does not prove UniversalFiberEntropyGap.",
        "It does not prove P vs NP or any Clay-problem result.",
    ]

    for token in required:
        assert token in doc


def test_forbidden_overclaim_tokens_absent():
    combined = DOC.read_text() + json.dumps(json.loads(ARTIFACT.read_text()))

    forbidden = [
        "FinalCarrierDomainUniformArityBound is proved",
        "FinalCarrierDomainNormalForm implies UniformStratumDefect",
        "unrestricted Chronos-RR is proved",
        "H4.1/FGL is proved",
        "UniversalFiberEntropyGap is proved",
        "P vs NP is proved",
        "Clay problem solved",
    ]

    for token in forbidden:
        assert token not in combined
