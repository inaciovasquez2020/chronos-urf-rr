from pathlib import Path

def test_newstein_local_triangle_generation_lemma_doc():
    s = Path("docs/math/NEWSTEIN_LOCAL_TRIANGLE_GENERATION_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "L>2r+1" in s
    assert "\\operatorname{girth}(X_n)>2r+1" in s
    assert "lies in the \\(\\mathbb F_2\\)-span of triangle boundaries" in s
    assert "Z_1\\!\\bigl(B_r^{B_n}(x)\\bigr)" in s
    assert "The local triangle-generation lemma supplies item (1) in the Newstein local cycle-vanishing lemma." in s
    assert "No proof of the lemma is claimed here." in s
