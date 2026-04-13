from pathlib import Path

MOD = Path("docs/math/KAIROS_MODULE.md")
REG = Path("docs/status/KAIROS_TOOLKIT_REGISTRY.md")

def test_kairos_module_lock():
    text = MOD.read_text()
    required = [
        "Status: structural-module",
        "Scope: toolkit",
        "Role: canonical weakest-sufficient countereffect tool opposing drift, suppressing unstable amplification, and restoring admissible structure.",
        r"\mathcal K_{\Phi,\lambda}(X)=-\lambda \nabla \Phi(X)",
        "DriftOpposition",
        "AdmissibilityReturn",
        "RunawaySuppression",
        "LyapunovDecay",
        "WeakestSufficientCountereffect",
        "Kairos-R",
        "It is not a flagship closure claim.",
    ]
    for needle in required:
        assert needle in text, needle

def test_kairos_registry_lock():
    text = REG.read_text()
    required = [
        "Module: Kairos — Universal Countereffect Stabilization Module",
        "Status: structural-module",
        "Classification: toolkit",
        "Canonical doc: docs/math/KAIROS_MODULE.md",
        "Certified instance: docs/math/KAIROS_2D_NS_STABILIZATION.md",
        "Kairos is the canonical weakest-sufficient countereffect restoring admissible structure under measured instability.",
        "Kairos does not by itself count as a frontier closure, flagship completion, or terminal obstruction discharge.",
    ]
    for needle in required:
        assert needle in text, needle
