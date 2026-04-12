from pathlib import Path

def test_newstein_fiber_to_global_injection_lemma_doc():
    s = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTION_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "\\iota_v^{\\mathrm{triv}}" in s
    assert "\\iota_v^{\\mathrm{tw}}" in s
    assert "is injective" in s
    assert "\\dim Q(G_n)-\\dim Q(H_n)\\ge 2|V(X_n)|." in s
    assert "No proof of the lemma is claimed here." in s
