from pathlib import Path

def test_newstein_path_integration_lemma_doc():
    s = Path("docs/math/NEWSTEIN_PATH_INTEGRATION_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "\\phi(C)=0" in s
    assert "f(x):=\\sum_{e\\in P_{x_0,x}} \\phi(e)\\in \\mathbb F_2" in s
    assert "\\phi(uv)=f(u)+f(v)." in s
    assert "\\phi=\\delta f." in s
    assert "The path-integration lemma implies the Newstein local coboundary criterion." in s
    assert "No proof of the lemma is claimed here." in s
