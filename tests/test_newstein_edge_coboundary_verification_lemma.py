from pathlib import Path

def test_newstein_edge_coboundary_verification_lemma_doc():
    s = Path("docs/math/NEWSTEIN_EDGE_COBOUNDARY_VERIFICATION_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "f(x):=\\sum_{e\\in P_{x_0,x}}\\phi(e)\\in\\mathbb F_2" in s
    assert "\\phi(uv)=f(u)+f(v)." in s
    assert "\\phi=\\delta f." in s
    assert "The edge-coboundary verification lemma supplies the final step in the Newstein path-integration lemma." in s
    assert "No proof of the lemma is claimed here." in s
