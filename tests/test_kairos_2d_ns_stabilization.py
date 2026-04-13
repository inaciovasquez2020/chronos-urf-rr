from pathlib import Path

DOC = Path("docs/math/KAIROS_2D_NS_STABILIZATION.md")

def test_kairos_2d_ns_stabilization_lock():
    text = DOC.read_text()
    required = [
        "Status: supporting-instance",
        "Scope: non-frontier",
        "Role: certified strong test of the Kairos stabilization tool; not a flagship closure claim.",
        r"\mathcal K(u)=-\lambda \mathbb P u.",
        r"\partial_t\omega+u\cdot\nabla\omega=\nu\Delta\omega-\lambda\omega.",
        "tool-validation",
        "certified-test-case",
        "It does not count as a frontier closure or flagship program completion.",
    ]
    for needle in required:
        assert needle in text, needle
