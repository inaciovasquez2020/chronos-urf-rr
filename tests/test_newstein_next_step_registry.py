from pathlib import Path

def test_newstein_next_step_registry_lock():
    text = Path("docs/status/NEWSTEIN_NEXT_STEP_REGISTRY.md").read_text(encoding="utf-8")
    assert "NEWSTEIN_EXACT_MISSING_OBJECT.md" in text
    assert "\\Phi_m(x_0,\\dots,x_m)" in text
    assert "\\forall I\\subseteq\\{0,\\dots,m\\}" in text
    assert "\\text{OPEN}." in text
    assert "No theorem-level promotion is licensed before }\\Phi_m\\text{ is fixed explicitly." in text
