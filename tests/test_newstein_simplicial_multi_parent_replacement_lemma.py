from pathlib import Path

def test_newstein_simplicial_multi_parent_replacement_lemma_lock():
    text = Path("docs/math/NEWSTEIN_SIMPLICIAL_MULTI_PARENT_REPLACEMENT_LEMMA.md").read_text(encoding="utf-8")
    assert "forall I\\subseteq\\{0,\\dots,m\\}" in text
    assert "I=\\{j\\}" in text
    assert "I=\\{0,\\dots,m\\}" in text
    assert "\\text{OPEN}." in text
